from __future__ import annotations

import json
from datetime import datetime, timezone
from textwrap import wrap
from typing import Any, Literal
import re

import click
from click.core import ParameterSource  # type: ignore[attr-defined]
from rich import print as rprint
from tabulate import tabulate

from together import Together
from together.cli.api.utils import BOOL_WITH_AUTO, INT_WITH_MAX
from together.utils import (
    finetune_price_to_dollars,
    log_warn,
    log_warn_once,
    parse_timestamp,
    format_timestamp,
)
from together.types.finetune import (
    DownloadCheckpointType,
    FinetuneTrainingLimits,
    FinetuneEventType,
)


_CONFIRMATION_MESSAGE = (
    "You are about to create a fine-tuning job. "
    "The cost of your job will be determined by the model size, the number of tokens "
    "in the training file, the number of tokens in the validation file, the number of epochs, and "
    "the number of evaluations. Visit https://www.together.ai/pricing to get a price estimate.\n"
    "You can pass `-y` or `--confirm` to your command to skip this message.\n\n"
    "Do you want to proceed?"
)


class DownloadCheckpointTypeChoice(click.Choice):
    def __init__(self) -> None:
        super().__init__([ct.value for ct in DownloadCheckpointType])

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> DownloadCheckpointType:
        value = super().convert(value, param, ctx)
        return DownloadCheckpointType(value)


@click.group(name="fine-tuning")
@click.pass_context
def fine_tuning(ctx: click.Context) -> None:
    """Fine-tunes API commands"""
    pass


@fine_tuning.command()
@click.pass_context
@click.option(
    "--training-file", type=str, required=True, help="Training file ID from Files API"
)
@click.option("--model", type=str, required=True, help="Base model name")
@click.option("--n-epochs", type=int, default=1, help="Number of epochs to train for")
@click.option(
    "--validation-file", type=str, default="", help="Validation file ID from Files API"
)
@click.option("--n-evals", type=int, default=0, help="Number of evaluation loops")
@click.option(
    "--n-checkpoints", type=int, default=1, help="Number of checkpoints to save"
)
@click.option("--batch-size", type=INT_WITH_MAX, default="max", help="Train batch size")
@click.option("--learning-rate", type=float, default=1e-5, help="Learning rate")
@click.option(
    "--min-lr-ratio",
    type=float,
    default=0.0,
    help="The ratio of the final learning rate to the peak learning rate",
)
@click.option(
    "--warmup-ratio",
    type=float,
    default=0.0,
    help="Warmup ratio for learning rate scheduler.",
)
@click.option(
    "--max-grad-norm",
    type=float,
    default=1.0,
    help="Max gradient norm to be used for gradient clipping. Set to 0 to disable.",
)
@click.option(
    "--weight-decay",
    type=float,
    default=0.0,
    help="Weight decay",
)
@click.option(
    "--lora/--no-lora",
    type=bool,
    default=True,
    help="Whether to use LoRA adapters for fine-tuning",
)
@click.option("--lora-r", type=int, default=8, help="LoRA adapters' rank")
@click.option("--lora-dropout", type=float, default=0, help="LoRA adapters' dropout")
@click.option("--lora-alpha", type=float, default=8, help="LoRA adapters' alpha")
@click.option(
    "--lora-trainable-modules",
    type=str,
    default="all-linear",
    help="Trainable modules for LoRA adapters. For example, 'all-linear', 'q_proj,v_proj'",
)
@click.option(
    "--training-method",
    type=click.Choice(["sft", "dpo"]),
    default="sft",
    help="Training method to use. Options: sft (supervised fine-tuning), dpo (Direct Preference Optimization)",
)
@click.option(
    "--dpo-beta",
    type=float,
    default=0.1,
    help="Beta parameter for DPO training (only used when '--training-method' is 'dpo')",
)
@click.option(
    "--suffix", type=str, default=None, help="Suffix for the fine-tuned model name"
)
@click.option("--wandb-api-key", type=str, default=None, help="Wandb API key")
@click.option("--wandb-base-url", type=str, default=None, help="Wandb base URL")
@click.option("--wandb-project-name", type=str, default=None, help="Wandb project name")
@click.option("--wandb-name", type=str, default=None, help="Wandb run name")
@click.option(
    "--confirm",
    "-y",
    type=bool,
    is_flag=True,
    default=False,
    help="Whether to skip the launch confirmation message",
)
@click.option(
    "--train-on-inputs",
    type=BOOL_WITH_AUTO,
    default="auto",
    help="Whether to mask the user messages in conversational data or prompts in instruction data. "
    "`auto` will automatically determine whether to mask the inputs based on the data format.",
)
@click.option(
    "--from-checkpoint",
    type=str,
    default=None,
    help="The checkpoint identifier to continue training from a previous fine-tuning job. "
    "The format: {$JOB_ID/$OUTPUT_MODEL_NAME}:{$STEP}. "
    "The step value is optional, without it the final checkpoint will be used.",
)
def create(
    ctx: click.Context,
    training_file: str,
    validation_file: str,
    model: str,
    n_epochs: int,
    n_evals: int,
    n_checkpoints: int,
    batch_size: int | Literal["max"],
    learning_rate: float,
    min_lr_ratio: float,
    warmup_ratio: float,
    max_grad_norm: float,
    weight_decay: float,
    lora: bool,
    lora_r: int,
    lora_dropout: float,
    lora_alpha: float,
    lora_trainable_modules: str,
    suffix: str,
    wandb_api_key: str,
    wandb_base_url: str,
    wandb_project_name: str,
    wandb_name: str,
    confirm: bool,
    train_on_inputs: bool | Literal["auto"],
    training_method: str,
    dpo_beta: float,
    from_checkpoint: str,
) -> None:
    """Start fine-tuning"""
    client: Together = ctx.obj

    training_args: dict[str, Any] = dict(
        training_file=training_file,
        model=model,
        n_epochs=n_epochs,
        validation_file=validation_file,
        n_evals=n_evals,
        n_checkpoints=n_checkpoints,
        batch_size=batch_size,
        learning_rate=learning_rate,
        min_lr_ratio=min_lr_ratio,
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
        from_checkpoint=from_checkpoint,
    )

    model_limits: FinetuneTrainingLimits = client.fine_tuning.get_model_limits(
        model=model
    )

    if lora:
        if model_limits.lora_training is None:
            raise click.BadParameter(
                f"LoRA fine-tuning is not supported for the model `{model}`"
            )

        default_values = {
            "lora_r": model_limits.lora_training.max_rank,
            "batch_size": model_limits.lora_training.max_batch_size,
            "learning_rate": 1e-3,
        }

        for arg in default_values:
            arg_source = ctx.get_parameter_source("arg")  # type: ignore[attr-defined]
            if arg_source == ParameterSource.DEFAULT:
                training_args[arg] = default_values[arg_source]

        if ctx.get_parameter_source("lora_alpha") == ParameterSource.DEFAULT:  # type: ignore[attr-defined]
            training_args["lora_alpha"] = training_args["lora_r"] * 2
    else:
        if model_limits.full_training is None:
            raise click.BadParameter(
                f"Full fine-tuning is not supported for the model `{model}`"
            )

        for param in ["lora_r", "lora_dropout", "lora_alpha", "lora_trainable_modules"]:
            param_source = ctx.get_parameter_source(param)  # type: ignore[attr-defined]
            if param_source != ParameterSource.DEFAULT:
                raise click.BadParameter(
                    f"You set LoRA parameter `{param}` for a full fine-tuning job. "
                    f"Please change the job type with --lora or remove `{param}` from the arguments"
                )

        batch_size_source = ctx.get_parameter_source("batch_size")  # type: ignore[attr-defined]
        if batch_size_source == ParameterSource.DEFAULT:
            training_args["batch_size"] = model_limits.full_training.max_batch_size

    if n_evals <= 0 and validation_file:
        log_warn(
            "Warning: You have specified a validation file but the number of evaluation loops is set to 0. No evaluations will be performed."
        )
    elif n_evals > 0 and not validation_file:
        raise click.BadParameter(
            "You have specified a number of evaluation loops but no validation file."
        )

    if confirm or click.confirm(_CONFIRMATION_MESSAGE, default=True, show_default=True):
        response = client.fine_tuning.create(
            **training_args,
            verbose=True,
        )

        report_string = f"Successfully submitted a fine-tuning job {response.id}"
        if response.created_at is not None:
            created_time = datetime.strptime(
                response.created_at, "%Y-%m-%dT%H:%M:%S.%f%z"
            )
            # created_at reports UTC time, we use .astimezone() to convert to local time
            formatted_time = created_time.astimezone().strftime("%m/%d/%Y, %H:%M:%S")
            report_string += f" at {formatted_time}"
        rprint(report_string)
    else:
        click.echo("No confirmation received, stopping job launch")


@fine_tuning.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List fine-tuning jobs"""
    client: Together = ctx.obj

    response = client.fine_tuning.list()

    response.data = response.data or []

    # Use a default datetime for None values to make sure the key function always returns a comparable value
    epoch_start = datetime.fromtimestamp(0, tz=timezone.utc)
    response.data.sort(key=lambda x: parse_timestamp(x.created_at or "") or epoch_start)

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Fine-tune ID": i.id,
                "Model Output Name": "\n".join(wrap(i.output_name or "", width=30)),
                "Status": i.status,
                "Created At": i.created_at,
                "Price": f"""${finetune_price_to_dollars(
                    float(str(i.total_price))
                )}""",  # convert to string for mypy typing
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def retrieve(ctx: click.Context, fine_tune_id: str) -> None:
    """Retrieve fine-tuning job details"""
    client: Together = ctx.obj

    response = client.fine_tuning.retrieve(fine_tune_id)

    # remove events from response for cleaner output
    response.events = None

    click.echo(json.dumps(response.model_dump(exclude_none=True), indent=4))


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
@click.option(
    "--quiet", is_flag=True, help="Do not prompt for confirmation before cancelling job"
)
def cancel(ctx: click.Context, fine_tune_id: str, quiet: bool = False) -> None:
    """Cancel fine-tuning job"""
    client: Together = ctx.obj
    if not quiet:
        confirm_response = input(
            "You will be billed for any completed training steps upon cancellation. "
            f"Do you want to cancel job {fine_tune_id}? [y/N]"
        )
        if "y" not in confirm_response.lower():
            click.echo({"status": "Cancel not submitted"})
            return
    response = client.fine_tuning.cancel(fine_tune_id)

    click.echo(json.dumps(response.model_dump(exclude_none=True), indent=4))


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def list_events(ctx: click.Context, fine_tune_id: str) -> None:
    """List fine-tuning events"""
    client: Together = ctx.obj

    response = client.fine_tuning.list_events(fine_tune_id)

    response.data = response.data or []

    display_list = []
    for i in response.data:
        display_list.append(
            {
                "Message": "\n".join(wrap(i.message or "", width=50)),
                "Type": i.type,
                "Created At": parse_timestamp(i.created_at or ""),
                "Hash": i.hash,
            }
        )
    table = tabulate(display_list, headers="keys", tablefmt="grid", showindex=True)

    click.echo(table)


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
def list_checkpoints(ctx: click.Context, fine_tune_id: str) -> None:
    """List available checkpoints for a fine-tuning job"""
    client: Together = ctx.obj

    checkpoints = client.fine_tuning.list_checkpoints(fine_tune_id)

    display_list = []
    for checkpoint in checkpoints:
        display_list.append(
            {
                "Type": checkpoint.type,
                "Timestamp": format_timestamp(checkpoint.timestamp),
                "Name": checkpoint.name,
            }
        )

    if display_list:
        click.echo(f"Job {fine_tune_id} contains the following checkpoints:")
        table = tabulate(display_list, headers="keys", tablefmt="grid")
        click.echo(table)
        click.echo("\nTo download a checkpoint, use `together fine-tuning download`")
    else:
        click.echo(f"No checkpoints found for job {fine_tune_id}")


@fine_tuning.command()
@click.pass_context
@click.argument("fine_tune_id", type=str, required=True)
@click.option(
    "--output_dir",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    required=False,
    default=None,
    help="Output directory",
)
@click.option(
    "--checkpoint-step",
    type=int,
    required=False,
    default=None,
    help="Download fine-tuning checkpoint. Defaults to latest.",
)
@click.option(
    "--checkpoint-type",
    type=DownloadCheckpointTypeChoice(),
    required=False,
    default=DownloadCheckpointType.DEFAULT.value,
    help="Specifies checkpoint type. 'merged' and 'adapter' options work only for LoRA jobs.",
)
def download(
    ctx: click.Context,
    fine_tune_id: str,
    output_dir: str,
    checkpoint_step: int | None,
    checkpoint_type: DownloadCheckpointType,
) -> None:
    """Download fine-tuning checkpoint"""
    client: Together = ctx.obj

    response = client.fine_tuning.download(
        fine_tune_id,
        output=output_dir,
        checkpoint_step=checkpoint_step,
        checkpoint_type=checkpoint_type,
    )

    click.echo(json.dumps(response.model_dump(exclude_none=True), indent=4))
