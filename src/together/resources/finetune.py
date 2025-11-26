from __future__ import annotations

import re
from pathlib import Path
from typing import List, Dict, Literal

from rich import print as rprint

from together.abstract import api_requestor
from together.filemanager import DownloadManager
from together.together_response import TogetherResponse
from together.types import (
    CosineLRScheduler,
    CosineLRSchedulerArgs,
    FinetuneCheckpoint,
    FinetuneDeleteResponse,
    FinetuneDownloadResult,
    FinetuneList,
    FinetuneListEvents,
    FinetuneLRScheduler,
    FinetuneRequest,
    FinetuneResponse,
    FinetuneTrainingLimits,
    FullTrainingType,
    LinearLRScheduler,
    LinearLRSchedulerArgs,
    LoRATrainingType,
    TogetherClient,
    TogetherRequest,
    TrainingMethodDPO,
    TrainingMethodSFT,
    TrainingType,
)
from together.types.finetune import DownloadCheckpointType
from together.utils import log_warn_once, normalize_key


_FT_JOB_WITH_STEP_REGEX = r"^ft-[\dabcdef-]+:\d+$"


AVAILABLE_TRAINING_METHODS = {
    TrainingMethodSFT().method,
    TrainingMethodDPO().method,
}


def create_finetune_request(
    model_limits: FinetuneTrainingLimits,
    training_file: str,
    model: str | None = None,
    n_epochs: int = 1,
    validation_file: str | None = "",
    n_evals: int | None = 0,
    n_checkpoints: int | None = 1,
    batch_size: int | Literal["max"] = "max",
    learning_rate: float | None = 0.00001,
    lr_scheduler_type: Literal["linear", "cosine"] = "cosine",
    min_lr_ratio: float = 0.0,
    scheduler_num_cycles: float = 0.5,
    warmup_ratio: float | None = None,
    max_grad_norm: float = 1.0,
    weight_decay: float = 0.0,
    lora: bool = False,
    lora_r: int | None = None,
    lora_dropout: float | None = 0,
    lora_alpha: float | None = None,
    lora_trainable_modules: str | None = "all-linear",
    suffix: str | None = None,
    wandb_api_key: str | None = None,
    wandb_base_url: str | None = None,
    wandb_project_name: str | None = None,
    wandb_name: str | None = None,
    train_on_inputs: bool | Literal["auto"] | None = None,
    training_method: str = "sft",
    dpo_beta: float | None = None,
    dpo_normalize_logratios_by_length: bool = False,
    rpo_alpha: float | None = None,
    simpo_gamma: float | None = None,
    from_checkpoint: str | None = None,
    from_hf_model: str | None = None,
    hf_model_revision: str | None = None,
    hf_api_token: str | None = None,
    hf_output_repo_name: str | None = None,
) -> FinetuneRequest:
    if model is not None and from_checkpoint is not None:
        raise ValueError(
            "You must specify either a model or a checkpoint to start a job from, not both"
        )

    if model is None and from_checkpoint is None:
        raise ValueError("You must specify either a model or a checkpoint")

    if from_checkpoint is not None and from_hf_model is not None:
        raise ValueError(
            "You must specify either a Hugging Face Hub model or a previous checkpoint from "
            "Together to start a job from, not both"
        )

    if from_hf_model is not None and model is None:
        raise ValueError(
            "You must specify the base model to fine-tune a model from the Hugging Face Hub"
        )

    model_or_checkpoint = model or from_checkpoint

    if warmup_ratio is None:
        warmup_ratio = 0.0

    training_type: TrainingType = FullTrainingType()
    if lora:
        if model_limits.lora_training is None:
            raise ValueError(
                f"LoRA adapters are not supported for the selected model ({model_or_checkpoint})."
            )

        if lora_dropout is not None:
            if not 0 <= lora_dropout < 1.0:
                raise ValueError("LoRA dropout must be in [0, 1) range.")

        lora_r = lora_r if lora_r is not None else model_limits.lora_training.max_rank
        lora_alpha = lora_alpha if lora_alpha is not None else lora_r * 2
        training_type = LoRATrainingType(
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            lora_trainable_modules=lora_trainable_modules,
        )

        max_batch_size = model_limits.lora_training.max_batch_size
        min_batch_size = model_limits.lora_training.min_batch_size
        max_batch_size_dpo = model_limits.lora_training.max_batch_size_dpo
    else:
        if model_limits.full_training is None:
            raise ValueError(
                f"Full training is not supported for the selected model ({model_or_checkpoint})."
            )

        max_batch_size = model_limits.full_training.max_batch_size
        min_batch_size = model_limits.full_training.min_batch_size
        max_batch_size_dpo = model_limits.full_training.max_batch_size_dpo

    if batch_size != "max":
        if training_method == "sft":
            if batch_size > max_batch_size:
                raise ValueError(
                    f"Requested batch size of {batch_size} is higher that the maximum allowed value of {max_batch_size}."
                )
        elif training_method == "dpo":
            if batch_size > max_batch_size_dpo:
                raise ValueError(
                    f"Requested batch size of {batch_size} is higher that the maximum allowed value of {max_batch_size_dpo}."
                )

        if batch_size < min_batch_size:
            raise ValueError(
                f"Requested batch size of {batch_size} is lower that the minimum allowed value of {min_batch_size}."
            )

    if warmup_ratio > 1 or warmup_ratio < 0:
        raise ValueError(f"Warmup ratio should be between 0 and 1 (got {warmup_ratio})")

    if min_lr_ratio is not None and (min_lr_ratio > 1 or min_lr_ratio < 0):
        raise ValueError(
            f"Min learning rate ratio should be between 0 and 1 (got {min_lr_ratio})"
        )

    if max_grad_norm < 0:
        raise ValueError(
            f"Max gradient norm should be non-negative (got {max_grad_norm})"
        )

    if weight_decay is not None and (weight_decay < 0):
        raise ValueError(f"Weight decay should be non-negative (got {weight_decay})")

    if training_method not in AVAILABLE_TRAINING_METHODS:
        raise ValueError(
            f"training_method must be one of {', '.join(AVAILABLE_TRAINING_METHODS)}"
        )

    if train_on_inputs is not None and training_method != "sft":
        raise ValueError("train_on_inputs is only supported for SFT training")

    if train_on_inputs is None and training_method == "sft":
        log_warn_once(
            "train_on_inputs is not set for SFT training, it will be set to 'auto'"
        )
        train_on_inputs = "auto"

    if dpo_beta is not None and training_method != "dpo":
        raise ValueError("dpo_beta is only supported for DPO training")
    if dpo_normalize_logratios_by_length and training_method != "dpo":
        raise ValueError(
            "dpo_normalize_logratios_by_length=True is only supported for DPO training"
        )
    if rpo_alpha is not None:
        if training_method != "dpo":
            raise ValueError("rpo_alpha is only supported for DPO training")
        if not rpo_alpha >= 0.0:
            raise ValueError(f"rpo_alpha should be non-negative (got {rpo_alpha})")

    if simpo_gamma is not None:
        if training_method != "dpo":
            raise ValueError("simpo_gamma is only supported for DPO training")
        if not simpo_gamma >= 0.0:
            raise ValueError(f"simpo_gamma should be non-negative (got {simpo_gamma})")

    lr_scheduler: FinetuneLRScheduler
    if lr_scheduler_type == "cosine":
        if scheduler_num_cycles <= 0.0:
            raise ValueError(
                f"Number of cycles should be greater than 0 (got {scheduler_num_cycles})"
            )

        lr_scheduler = CosineLRScheduler(
            lr_scheduler_args=CosineLRSchedulerArgs(
                min_lr_ratio=min_lr_ratio, num_cycles=scheduler_num_cycles
            ),
        )
    else:
        lr_scheduler = LinearLRScheduler(
            lr_scheduler_args=LinearLRSchedulerArgs(min_lr_ratio=min_lr_ratio),
        )

    training_method_cls: TrainingMethodSFT | TrainingMethodDPO
    if training_method == "sft":
        training_method_cls = TrainingMethodSFT(train_on_inputs=train_on_inputs)
    elif training_method == "dpo":
        if simpo_gamma is not None and simpo_gamma > 0:
            dpo_reference_free = True
            dpo_normalize_logratios_by_length = True
            rprint(
                f"Parameter simpo_gamma was set to {simpo_gamma}. "
                "SimPO training detected. Reference logits will not be used "
                "and length normalization of log-probabilities will be enabled."
            )
        else:
            dpo_reference_free = False

        training_method_cls = TrainingMethodDPO(
            dpo_beta=dpo_beta,
            dpo_normalize_logratios_by_length=dpo_normalize_logratios_by_length,
            dpo_reference_free=dpo_reference_free,
            rpo_alpha=rpo_alpha,
            simpo_gamma=simpo_gamma,
        )

    finetune_request = FinetuneRequest(
        model=model,
        training_file=training_file,
        validation_file=validation_file,
        n_epochs=n_epochs,
        n_evals=n_evals,
        n_checkpoints=n_checkpoints,
        batch_size=batch_size,
        learning_rate=learning_rate,
        lr_scheduler=lr_scheduler,
        warmup_ratio=warmup_ratio,
        max_grad_norm=max_grad_norm,
        weight_decay=weight_decay,
        training_type=training_type,
        suffix=suffix,
        wandb_key=wandb_api_key,
        wandb_base_url=wandb_base_url,
        wandb_project_name=wandb_project_name,
        wandb_name=wandb_name,
        training_method=training_method_cls,
        from_checkpoint=from_checkpoint,
        from_hf_model=from_hf_model,
        hf_model_revision=hf_model_revision,
        hf_api_token=hf_api_token,
        hf_output_repo_name=hf_output_repo_name,
    )

    return finetune_request


def _parse_raw_checkpoints(
    checkpoints: List[Dict[str, str]], id: str
) -> List[FinetuneCheckpoint]:
    """
    Helper function to process raw checkpoints and create checkpoint list.

    Args:
        checkpoints (List[Dict[str, str]]): List of raw checkpoints metadata
        id (str): Fine-tune job ID

    Returns:
        List[FinetuneCheckpoint]: List of available checkpoints
    """

    parsed_checkpoints = []
    for checkpoint in checkpoints:
        step = checkpoint["step"]
        checkpoint_type = checkpoint["checkpoint_type"]
        checkpoint_name = (
            f"{id}:{step}" if "intermediate" in checkpoint_type.lower() else id
        )

        parsed_checkpoints.append(
            FinetuneCheckpoint(
                type=checkpoint_type,
                timestamp=checkpoint["created_at"],
                name=checkpoint_name,
            )
        )

    parsed_checkpoints.sort(key=lambda x: x.timestamp, reverse=True)
    return parsed_checkpoints


class FineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        *,
        training_file: str,
        model: str | None = None,
        n_epochs: int = 1,
        validation_file: str | None = "",
        n_evals: int | None = 0,
        n_checkpoints: int | None = 1,
        batch_size: int | Literal["max"] = "max",
        learning_rate: float | None = 0.00001,
        lr_scheduler_type: Literal["linear", "cosine"] = "cosine",
        min_lr_ratio: float = 0.0,
        scheduler_num_cycles: float = 0.5,
        warmup_ratio: float = 0.0,
        max_grad_norm: float = 1.0,
        weight_decay: float = 0.0,
        lora: bool = True,
        lora_r: int | None = None,
        lora_dropout: float | None = 0,
        lora_alpha: float | None = None,
        lora_trainable_modules: str | None = "all-linear",
        suffix: str | None = None,
        wandb_api_key: str | None = None,
        wandb_base_url: str | None = None,
        wandb_project_name: str | None = None,
        wandb_name: str | None = None,
        verbose: bool = False,
        model_limits: FinetuneTrainingLimits | None = None,
        train_on_inputs: bool | Literal["auto"] | None = None,
        training_method: str = "sft",
        dpo_beta: float | None = None,
        dpo_normalize_logratios_by_length: bool = False,
        rpo_alpha: float | None = None,
        simpo_gamma: float | None = None,
        from_checkpoint: str | None = None,
        from_hf_model: str | None = None,
        hf_model_revision: str | None = None,
        hf_api_token: str | None = None,
        hf_output_repo_name: str | None = None,
    ) -> FinetuneResponse:
        """
        Method to initiate a fine-tuning job

        Args:
            training_file (str): File-ID of a file uploaded to the Together API
            model (str, optional): Name of the base model to run fine-tune job on
            n_epochs (int, optional): Number of epochs for fine-tuning. Defaults to 1.
            validation file (str, optional): File ID of a file uploaded to the Together API for validation.
            n_evals (int, optional): Number of evaluation loops to run. Defaults to 0.
            n_checkpoints (int, optional): Number of checkpoints to save during fine-tuning.
                Defaults to 1.
            batch_size (int or "max"): Batch size for fine-tuning. Defaults to max.
            learning_rate (float, optional): Learning rate multiplier to use for training
                Defaults to 0.00001.
            lr_scheduler_type (Literal["linear", "cosine"]): Learning rate scheduler type. Defaults to "cosine".
            min_lr_ratio (float, optional): Min learning rate ratio of the initial learning rate for
                the learning rate scheduler. Defaults to 0.0.
            scheduler_num_cycles (float, optional): Number or fraction of cycles for the cosine learning rate scheduler. Defaults to 0.5.
            warmup_ratio (float, optional): Warmup ratio for the learning rate scheduler.
            max_grad_norm (float, optional): Max gradient norm. Defaults to 1.0, set to 0 to disable.
            weight_decay (float, optional): Weight decay. Defaults to 0.0.
            lora (bool, optional): Whether to use LoRA adapters. Defaults to True.
            lora_r (int, optional): Rank of LoRA adapters. Defaults to 8.
            lora_dropout (float, optional): Dropout rate for LoRA adapters. Defaults to 0.
            lora_alpha (float, optional): Alpha for LoRA adapters. Defaults to 8.
            lora_trainable_modules (str, optional): Trainable modules for LoRA adapters. Defaults to "all-linear".
            suffix (str, optional): Up to 40 character suffix that will be added to your fine-tuned model name.
                Defaults to None.
            wandb_api_key (str, optional): API key for Weights & Biases integration.
                Defaults to None.
            wandb_base_url (str, optional): Base URL for Weights & Biases integration.
                Defaults to None.
            wandb_project_name (str, optional): Project name for Weights & Biases integration.
                Defaults to None.
            wandb_name (str, optional): Run name for Weights & Biases integration.
                Defaults to None.
            verbose (bool, optional): whether to print the job parameters before submitting a request.
                Defaults to False.
            model_limits (FinetuneTrainingLimits, optional): Limits for the hyperparameters the model in Fine-tuning.
                Defaults to None.
            train_on_inputs (bool or "auto", optional): Whether to mask the user messages in conversational data or prompts in instruction data.
                "auto" will automatically determine whether to mask the inputs based on the data format.
                For datasets with the "text" field (general format), inputs will not be masked.
                For datasets with the "messages" field (conversational format) or "prompt" and "completion" fields
                (Instruction format), inputs will be masked.
                Defaults to None, or "auto" if training_method is "sft" (set in create_finetune_request).
            training_method (str, optional): Training method. Defaults to "sft".
                Supported methods: "sft", "dpo".
            dpo_beta (float, optional): DPO beta parameter. Defaults to None.
            dpo_normalize_logratios_by_length (bool): Whether or not normalize logratios by sample length. Defaults to False,
            rpo_alpha (float, optional): RPO alpha parameter of DPO training to include NLL in the loss. Defaults to None.
            simpo_gamma: (float, optional): SimPO gamma parameter. Defaults to None.
            from_checkpoint (str, optional): The checkpoint identifier to continue training from a previous fine-tuning job.
                The format: {$JOB_ID/$OUTPUT_MODEL_NAME}:{$STEP}.
                The step value is optional, without it the final checkpoint will be used.
            from_hf_model (str, optional): The Hugging Face Hub repo to start training from.
                Should be as close as possible to the base model (specified by the `model` argument) in terms of architecture and size.
            hf_model_revision (str, optional): The revision of the Hugging Face Hub model to continue training from. Defaults to None.
                Example: hf_model_revision=None (defaults to the latest revision in `main`) or
                hf_model_revision="607a30d783dfa663caf39e06633721c8d4cfcd7e" (specific commit).
            hf_api_token (str, optional): API key for the Hugging Face Hub. Defaults to None.
            hf_output_repo_name (str, optional): HF repo to upload the fine-tuned model to. Defaults to None.

        Returns:
            FinetuneResponse: Object containing information about fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        if model_limits is None:
            # mypy doesn't understand that model or from_checkpoint is not None
            if model is not None:
                model_name = model
            elif from_checkpoint is not None:
                model_name = from_checkpoint.split(":")[0]
            else:
                # this branch is unreachable, but mypy doesn't know that
                pass
            model_limits = self.get_model_limits(model=model_name)

        finetune_request = create_finetune_request(
            model_limits=model_limits,
            training_file=training_file,
            model=model,
            n_epochs=n_epochs,
            validation_file=validation_file,
            n_evals=n_evals,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            lr_scheduler_type=lr_scheduler_type,
            min_lr_ratio=min_lr_ratio,
            scheduler_num_cycles=scheduler_num_cycles,
            warmup_ratio=warmup_ratio,
            max_grad_norm=max_grad_norm,
            weight_decay=weight_decay,
            lora=lora,
            lora_r=lora_r,
            lora_dropout=lora_dropout,
            lora_alpha=lora_alpha,
            lora_trainable_modules=lora_trainable_modules,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
            wandb_base_url=wandb_base_url,
            wandb_project_name=wandb_project_name,
            wandb_name=wandb_name,
            train_on_inputs=train_on_inputs,
            training_method=training_method,
            dpo_beta=dpo_beta,
            dpo_normalize_logratios_by_length=dpo_normalize_logratios_by_length,
            rpo_alpha=rpo_alpha,
            simpo_gamma=simpo_gamma,
            from_checkpoint=from_checkpoint,
            from_hf_model=from_hf_model,
            hf_model_revision=hf_model_revision,
            hf_api_token=hf_api_token,
            hf_output_repo_name=hf_output_repo_name,
        )

        if verbose:
            rprint(
                "Submitting a fine-tuning job with the following parameters:",
                finetune_request,
            )
        parameter_payload = finetune_request.model_dump(exclude_none=True)

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="fine-tunes",
                params=parameter_payload,
            ),
            stream=False,
        )
        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    def list(self) -> FinetuneList:
        """
        Lists fine-tune job history

        Returns:
            FinetuneList: Object containing a list of fine-tune jobs
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="fine-tunes",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneList(**response.data)

    def retrieve(self, id: str) -> FinetuneResponse:
        """
        Retrieves fine-tune job details

        Args:
            id (str): Fine-tune ID to retrieve. A string that starts with `ft-`.

        Returns:
            FinetuneResponse: Object containing information about fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    def cancel(self, id: str) -> FinetuneResponse:
        """
        Method to cancel a running fine-tuning job

        Args:
            id (str): Fine-tune ID to cancel. A string that starts with `ft-`.

        Returns:
            FinetuneResponse: Object containing information about cancelled fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url=f"fine-tunes/{id}/cancel",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    def delete(self, id: str, force: bool = False) -> FinetuneDeleteResponse:
        """
        Method to delete a fine-tuning job

        Args:
            id (str): Fine-tune ID to delete. A string that starts with `ft-`.
            force (bool, optional): Force deletion. Defaults to False.

        Returns:
            FinetuneDeleteResponse: Object containing deletion confirmation message.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params = {"force": str(force).lower()}

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="DELETE",
                url=f"fine-tunes/{id}",
                params=params,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneDeleteResponse(**response.data)

    def list_events(self, id: str) -> FinetuneListEvents:
        """
        Lists events of a fine-tune job

        Args:
            id (str): Fine-tune ID to list events for. A string that starts with `ft-`.

        Returns:
            FinetuneListEvents: Object containing list of fine-tune events
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{id}/events",
            ),
            stream=False,
        )
        assert isinstance(response, TogetherResponse)

        return FinetuneListEvents(**response.data)

    def list_checkpoints(self, id: str) -> List[FinetuneCheckpoint]:
        """
        List available checkpoints for a fine-tuning job

        Args:
            id (str): Unique identifier of the fine-tune job to list checkpoints for

        Returns:
            List[FinetuneCheckpoint]: List of available checkpoints
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{id}/checkpoints",
            ),
            stream=False,
        )
        assert isinstance(response, TogetherResponse)

        raw_checkpoints = response.data["data"]
        return _parse_raw_checkpoints(raw_checkpoints, id)

    def download(
        self,
        id: str,
        *,
        output: Path | str | None = None,
        checkpoint_step: int | None = None,
        checkpoint_type: DownloadCheckpointType | str = DownloadCheckpointType.DEFAULT,
    ) -> FinetuneDownloadResult:
        """
        Downloads compressed fine-tuned model or checkpoint to local disk.

        Defaults file location to `$PWD/{model_name}.{extension}`

        Args:
            id (str): Fine-tune ID to download. A string that starts with `ft-`.
            output (pathlib.Path | str, optional): Specifies output file name for downloaded model.
                Defaults to None.
            checkpoint_step (int, optional): Specifies step number for checkpoint to download.
                Defaults to -1 (download the final model)
            checkpoint_type (CheckpointType | str, optional): Specifies which checkpoint to download.
                Defaults to CheckpointType.DEFAULT.

        Returns:
            FinetuneDownloadResult: Object containing downloaded model metadata
        """

        if re.match(_FT_JOB_WITH_STEP_REGEX, id) is not None:
            if checkpoint_step is None:
                checkpoint_step = int(id.split(":")[1])
                id = id.split(":")[0]
            else:
                raise ValueError(
                    "Fine-tuning job ID {id} contains a colon to specify the step to download, but `checkpoint_step` "
                    "was also set. Remove one of the step specifiers to proceed."
                )

        url = f"finetune/download?ft_id={id}"

        if checkpoint_step is not None:
            url += f"&checkpoint_step={checkpoint_step}"

        ft_job = self.retrieve(id)

        # convert str to DownloadCheckpointType
        if isinstance(checkpoint_type, str):
            try:
                checkpoint_type = DownloadCheckpointType(checkpoint_type.lower())
            except ValueError:
                enum_strs = ", ".join(e.value for e in DownloadCheckpointType)
                raise ValueError(
                    f"Invalid checkpoint type: {checkpoint_type}. Choose one of {{{enum_strs}}}."
                )

        if isinstance(ft_job.training_type, FullTrainingType):
            if checkpoint_type != DownloadCheckpointType.DEFAULT:
                raise ValueError(
                    "Only DEFAULT checkpoint type is allowed for FullTrainingType"
                )
            url += "&checkpoint=model_output_path"
        elif isinstance(ft_job.training_type, LoRATrainingType):
            if checkpoint_type == DownloadCheckpointType.DEFAULT:
                checkpoint_type = DownloadCheckpointType.MERGED

            if checkpoint_type in {
                DownloadCheckpointType.MERGED,
                DownloadCheckpointType.ADAPTER,
            }:
                url += f"&checkpoint={checkpoint_type.value}"
            else:
                raise ValueError(
                    f"Invalid checkpoint type for LoRATrainingType: {checkpoint_type}"
                )

        remote_name = ft_job.output_name

        download_manager = DownloadManager(self._client)

        if isinstance(output, str):
            output = Path(output)

        downloaded_filename, file_size = download_manager.download(
            url, output, normalize_key(remote_name or id), fetch_metadata=True
        )

        return FinetuneDownloadResult(
            object="local",
            id=id,
            checkpoint_step=checkpoint_step,
            filename=downloaded_filename,
            size=file_size,
        )

    def get_model_limits(self, *, model: str) -> FinetuneTrainingLimits:
        """
        Requests training limits for a specific model

        Args:
            model_name (str): Name of the model to get limits for

        Returns:
            FinetuneTrainingLimits: Object containing training limits for the model
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        model_limits_response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="fine-tunes/models/limits",
                params={"model_name": model},
            ),
            stream=False,
        )

        model_limits = FinetuneTrainingLimits(**model_limits_response.data)

        return model_limits


class AsyncFineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        training_file: str,
        model: str | None = None,
        n_epochs: int = 1,
        validation_file: str | None = "",
        n_evals: int | None = 0,
        n_checkpoints: int | None = 1,
        batch_size: int | Literal["max"] = "max",
        learning_rate: float | None = 0.00001,
        lr_scheduler_type: Literal["linear", "cosine"] = "cosine",
        min_lr_ratio: float = 0.0,
        scheduler_num_cycles: float = 0.5,
        warmup_ratio: float = 0.0,
        max_grad_norm: float = 1.0,
        weight_decay: float = 0.0,
        lora: bool = True,
        lora_r: int | None = None,
        lora_dropout: float | None = 0,
        lora_alpha: float | None = None,
        lora_trainable_modules: str | None = "all-linear",
        suffix: str | None = None,
        wandb_api_key: str | None = None,
        wandb_base_url: str | None = None,
        wandb_project_name: str | None = None,
        wandb_name: str | None = None,
        verbose: bool = False,
        model_limits: FinetuneTrainingLimits | None = None,
        train_on_inputs: bool | Literal["auto"] | None = None,
        training_method: str = "sft",
        dpo_beta: float | None = None,
        dpo_normalize_logratios_by_length: bool = False,
        rpo_alpha: float | None = None,
        simpo_gamma: float | None = None,
        from_checkpoint: str | None = None,
        from_hf_model: str | None = None,
        hf_model_revision: str | None = None,
        hf_api_token: str | None = None,
        hf_output_repo_name: str | None = None,
    ) -> FinetuneResponse:
        """
        Async method to initiate a fine-tuning job

        Args:
            training_file (str): File-ID of a file uploaded to the Together API
            model (str, optional): Name of the base model to run fine-tune job on
            n_epochs (int, optional): Number of epochs for fine-tuning. Defaults to 1.
            validation file (str, optional): File ID of a file uploaded to the Together API for validation.
            n_evals (int, optional): Number of evaluation loops to run. Defaults to 0.
            n_checkpoints (int, optional): Number of checkpoints to save during fine-tuning.
                Defaults to 1.
            batch_size (int, optional): Batch size for fine-tuning. Defaults to max.
            learning_rate (float, optional): Learning rate multiplier to use for training
                Defaults to 0.00001.
            lr_scheduler_type (Literal["linear", "cosine"]): Learning rate scheduler type. Defaults to "cosine".
            min_lr_ratio (float, optional): Min learning rate ratio of the initial learning rate for
                the learning rate scheduler. Defaults to 0.0.
            scheduler_num_cycles (float, optional): Number or fraction of cycles for the cosine learning rate scheduler. Defaults to 0.5.
            warmup_ratio (float, optional): Warmup ratio for the learning rate scheduler.
            max_grad_norm (float, optional): Max gradient norm. Defaults to 1.0, set to 0 to disable.
            weight_decay (float, optional): Weight decay. Defaults to 0.0.
            lora (bool, optional): Whether to use LoRA adapters. Defaults to True.
            lora_r (int, optional): Rank of LoRA adapters. Defaults to 8.
            lora_dropout (float, optional): Dropout rate for LoRA adapters. Defaults to 0.
            lora_alpha (float, optional): Alpha for LoRA adapters. Defaults to 8.
            lora_trainable_modules (str, optional): Trainable modules for LoRA adapters. Defaults to "all-linear".
            suffix (str, optional): Up to 40 character suffix that will be added to your fine-tuned model name.
                Defaults to None.
            wandb_api_key (str, optional): API key for Weights & Biases integration.
                Defaults to None.
            wandb_base_url (str, optional): Base URL for Weights & Biases integration.
                Defaults to None.
            wandb_project_name (str, optional): Project name for Weights & Biases integration.
                Defaults to None.
            wandb_name (str, optional): Run name for Weights & Biases integration.
                Defaults to None.
            verbose (bool, optional): whether to print the job parameters before submitting a request.
                Defaults to False.
            model_limits (FinetuneTrainingLimits, optional): Limits for the hyperparameters the model in Fine-tuning.
                Defaults to None.
            train_on_inputs (bool or "auto"): Whether to mask the user messages in conversational data or prompts in instruction data.
                "auto" will automatically determine whether to mask the inputs based on the data format.
                For datasets with the "text" field (general format), inputs will not be masked.
                For datasets with the "messages" field (conversational format) or "prompt" and "completion" fields
                (Instruction format), inputs will be masked.
                Defaults to None, or "auto" if training_method is "sft" (set in create_finetune_request).
            training_method (str, optional): Training method. Defaults to "sft".
                Supported methods: "sft", "dpo".
            dpo_beta (float, optional): DPO beta parameter. Defaults to None.
            dpo_normalize_logratios_by_length (bool): Whether or not normalize logratios by sample length. Defaults to False,
            rpo_alpha (float, optional): RPO alpha parameter of DPO training to include NLL in the loss. Defaults to None.
            simpo_gamma: (float, optional): SimPO gamma parameter. Defaults to None.
            from_checkpoint (str, optional): The checkpoint identifier to continue training from a previous fine-tuning job.
                The format: {$JOB_ID/$OUTPUT_MODEL_NAME}:{$STEP}.
                The step value is optional, without it the final checkpoint will be used.
            from_hf_model (str, optional): The Hugging Face Hub repo to start training from.
                Should be as close as possible to the base model (specified by the `model` argument) in terms of architecture and size.
            hf_model_revision (str, optional): The revision of the Hugging Face Hub model to continue training from. Defaults to None.
                Example: hf_model_revision=None (defaults to the latest revision in `main`) or
                hf_model_revision="607a30d783dfa663caf39e06633721c8d4cfcd7e" (specific commit).
            hf_api_token (str, optional): API key for the Huggging Face Hub. Defaults to None.
            hf_output_repo_name (str, optional): HF repo to upload the fine-tuned model to. Defaults to None.

        Returns:
            FinetuneResponse: Object containing information about fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        if model_limits is None:
            # mypy doesn't understand that model or from_checkpoint is not None
            if model is not None:
                model_name = model
            elif from_checkpoint is not None:
                model_name = from_checkpoint.split(":")[0]
            else:
                # this branch is unreachable, but mypy doesn't know that
                pass
            model_limits = await self.get_model_limits(model=model_name)

        finetune_request = create_finetune_request(
            model_limits=model_limits,
            training_file=training_file,
            model=model,
            n_epochs=n_epochs,
            validation_file=validation_file,
            n_evals=n_evals,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            lr_scheduler_type=lr_scheduler_type,
            min_lr_ratio=min_lr_ratio,
            scheduler_num_cycles=scheduler_num_cycles,
            warmup_ratio=warmup_ratio,
            max_grad_norm=max_grad_norm,
            weight_decay=weight_decay,
            lora=lora,
            lora_r=lora_r,
            lora_dropout=lora_dropout,
            lora_alpha=lora_alpha,
            lora_trainable_modules=lora_trainable_modules,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
            wandb_base_url=wandb_base_url,
            wandb_project_name=wandb_project_name,
            wandb_name=wandb_name,
            train_on_inputs=train_on_inputs,
            training_method=training_method,
            dpo_beta=dpo_beta,
            dpo_normalize_logratios_by_length=dpo_normalize_logratios_by_length,
            rpo_alpha=rpo_alpha,
            simpo_gamma=simpo_gamma,
            from_checkpoint=from_checkpoint,
            from_hf_model=from_hf_model,
            hf_model_revision=hf_model_revision,
            hf_api_token=hf_api_token,
            hf_output_repo_name=hf_output_repo_name,
        )

        if verbose:
            rprint(
                "Submitting a fine-tuning job with the following parameters:",
                finetune_request,
            )
        parameter_payload = finetune_request.model_dump(exclude_none=True)

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="fine-tunes",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    async def list(self) -> FinetuneList:
        """
        Async method to list fine-tune job history

        Returns:
            FinetuneList: Object containing a list of fine-tune jobs
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="fine-tunes",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneList(**response.data)

    async def retrieve(self, id: str) -> FinetuneResponse:
        """
        Async method to retrieve fine-tune job details

        Args:
            id (str): Fine-tune ID to retrieve. A string that starts with `ft-`.

        Returns:
            FinetuneResponse: Object containing information about fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    async def cancel(self, id: str) -> FinetuneResponse:
        """
        Async method to cancel a running fine-tuning job

        Args:
            id (str): Fine-tune ID to cancel. A string that starts with `ft-`.

        Returns:
            FinetuneResponse: Object containing information about cancelled fine-tuning job.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url=f"fine-tunes/{id}/cancel",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneResponse(**response.data)

    async def delete(self, id: str, force: bool = False) -> FinetuneDeleteResponse:
        """
        Async method to delete a fine-tuning job

        Args:
            id (str): Fine-tune ID to delete. A string that starts with `ft-`.
            force (bool, optional): Force deletion. Defaults to False.

        Returns:
            FinetuneDeleteResponse: Object containing deletion confirmation message.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params = {"force": str(force).lower()}

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="DELETE",
                url=f"fine-tunes/{id}",
                params=params,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FinetuneDeleteResponse(**response.data)

    async def list_events(self, id: str) -> FinetuneListEvents:
        """
        List fine-tuning events

        Args:
            id (str): Unique identifier of the fine-tune job to list events for

        Returns:
            FinetuneListEvents: Object containing list of fine-tune job events
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        events_response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{normalize_key(id)}/events",
            ),
            stream=False,
        )
        assert isinstance(events_response, TogetherResponse)

        return FinetuneListEvents(**events_response.data)

    async def list_checkpoints(self, id: str) -> List[FinetuneCheckpoint]:
        """
        List available checkpoints for a fine-tuning job

        Args:
            id (str): Unique identifier of the fine-tune job to list checkpoints for

        Returns:
            List[FinetuneCheckpoint]: List of available checkpoints
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"fine-tunes/{id}/checkpoints",
            ),
            stream=False,
        )
        assert isinstance(response, TogetherResponse)

        raw_checkpoints = response.data["data"]
        return _parse_raw_checkpoints(raw_checkpoints, id)

    async def download(
        self, id: str, *, output: str | None = None, checkpoint_step: int = -1
    ) -> str:
        """
        TODO: Implement async download method
        """

        raise NotImplementedError(
            "AsyncFineTuning.download not implemented. "
            "Please use FineTuning.download function instead."
        )

    async def get_model_limits(self, *, model: str) -> FinetuneTrainingLimits:
        """
        Requests training limits for a specific model

        Args:
            model_name (str): Name of the model to get limits for

        Returns:
            FinetuneTrainingLimits: Object containing training limits for the model
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        model_limits_response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="fine-tunes/models/limits",
                params={"model": model},
            ),
            stream=False,
        )

        model_limits = FinetuneTrainingLimits(**model_limits_response.data)

        return model_limits
