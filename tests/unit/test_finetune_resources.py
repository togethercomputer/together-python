import pytest
from unittest.mock import MagicMock, Mock, patch

from together.client import Together
from together.resources.finetune import create_finetune_request
from together.together_response import TogetherResponse
from together.types import TogetherRequest
from together.types.finetune import (
    FinetuneFullTrainingLimits,
    FinetuneLoraTrainingLimits,
    FinetuneTrainingLimits,
)


_MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct-Reference"
_TRAINING_FILE = "file-7dbce5e9-7993-4520-9f3e-a7ece6c39d84"
_VALIDATION_FILE = "file-7dbce5e9-7553-4520-9f3e-a7ece6c39d84"
_FROM_CHECKPOINT = "ft-12345678-1234-1234-1234-1234567890ab"
_MODEL_LIMITS = FinetuneTrainingLimits(
    max_num_epochs=20,
    max_learning_rate=1.0,
    min_learning_rate=1e-6,
    full_training=FinetuneFullTrainingLimits(
        max_batch_size=96,
        max_batch_size_dpo=48,
        min_batch_size=8,
    ),
    lora_training=FinetuneLoraTrainingLimits(
        max_batch_size=128,
        max_batch_size_dpo=64,
        min_batch_size=8,
        max_rank=64,
        target_modules=["q", "k", "v", "o", "mlp"],
    ),
)


def mock_request(options: TogetherRequest, *args, **kwargs):
    if options.url == "fine-tunes/estimate-price":
        return (
            TogetherResponse(
                data={
                    "estimated_total_price": 100,
                    "allowed_to_proceed": True,
                    "estimated_train_token_count": 1000,
                    "estimated_eval_token_count": 100,
                    "user_limit": 1000,
                },
                headers={},
            ),
            None,
            None,
        )
    elif options.url == "fine-tunes":
        return (
            TogetherResponse(
                data={
                    "id": "ft-12345678-1234-1234-1234-1234567890ab",
                },
                headers={},
            ),
            None,
            None,
        )
    else:
        return (
            TogetherResponse(data=_MODEL_LIMITS.model_dump(), headers={}),
            None,
            None,
        )


def test_simple_request():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
    )

    assert request.model == _MODEL_NAME
    assert request.training_file == _TRAINING_FILE
    assert request.learning_rate > 0
    assert request.n_epochs > 0
    assert request.warmup_ratio == 0.0
    assert request.training_type.type == "Full"
    assert request.batch_size == "max"


def test_validation_file():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
        validation_file=_VALIDATION_FILE,
    )

    assert request.training_file == _TRAINING_FILE
    assert request.validation_file == _VALIDATION_FILE


def test_no_training_file():
    with pytest.raises(
        TypeError, match="missing 1 required positional argument: 'training_file'"
    ):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
        )


def test_lora_request():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
        lora=True,
    )

    assert request.training_type.type == "Lora"
    assert request.training_type.lora_r == _MODEL_LIMITS.lora_training.max_rank
    assert request.training_type.lora_alpha == _MODEL_LIMITS.lora_training.max_rank * 2
    assert request.training_type.lora_dropout == 0.0
    assert request.training_type.lora_trainable_modules == "all-linear"
    assert request.batch_size == "max"


@pytest.mark.parametrize("lora_dropout", [-1, 0, 0.5, 1.0, 10.0])
def test_lora_request_with_lora_dropout(lora_dropout: float):
    if 0 <= lora_dropout < 1:
        request = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            lora=True,
            lora_dropout=lora_dropout,
        )
        assert request.training_type.lora_dropout == lora_dropout
    else:
        with pytest.raises(
            ValueError,
            match=r"LoRA dropout must be in \[0, 1\) range.",
        ):
            create_finetune_request(
                model_limits=_MODEL_LIMITS,
                model=_MODEL_NAME,
                training_file=_TRAINING_FILE,
                lora=True,
                lora_dropout=lora_dropout,
            )


def test_dpo_request_lora():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
        training_method="dpo",
        lora=True,
    )

    assert request.training_type.type == "Lora"
    assert request.training_type.lora_r == _MODEL_LIMITS.lora_training.max_rank
    assert request.training_type.lora_alpha == _MODEL_LIMITS.lora_training.max_rank * 2
    assert request.training_type.lora_dropout == 0.0
    assert request.training_type.lora_trainable_modules == "all-linear"
    assert request.batch_size == "max"


def test_dpo_request():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
        training_method="dpo",
        lora=False,
    )

    assert request.training_type.type == "Full"
    assert request.batch_size == "max"


def test_from_checkpoint_request():
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        training_file=_TRAINING_FILE,
        from_checkpoint=_FROM_CHECKPOINT,
    )

    assert request.model is None
    assert request.from_checkpoint == _FROM_CHECKPOINT


def test_both_from_checkpoint_model_name():
    with pytest.raises(
        ValueError,
        match="You must specify either a model or a checkpoint to start a job from, not both",
    ):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            from_checkpoint=_FROM_CHECKPOINT,
        )


def test_no_from_checkpoint_no_model_name():
    with pytest.raises(
        ValueError, match="You must specify either a model or a checkpoint"
    ):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            training_file=_TRAINING_FILE,
        )


@pytest.mark.parametrize("batch_size", [256, 1])
@pytest.mark.parametrize("use_lora", [False, True])
def test_batch_size_limit(batch_size, use_lora):
    model_limits = (
        _MODEL_LIMITS.full_training if not use_lora else _MODEL_LIMITS.lora_training
    )
    max_batch_size = model_limits.max_batch_size
    min_batch_size = model_limits.min_batch_size

    if batch_size > max_batch_size:
        error_message = f"Requested batch size of {batch_size} is higher that the maximum allowed value of {max_batch_size}"
        with pytest.raises(ValueError, match=error_message):
            _ = create_finetune_request(
                model_limits=_MODEL_LIMITS,
                model=_MODEL_NAME,
                training_file=_TRAINING_FILE,
                batch_size=batch_size,
                lora=use_lora,
            )

    if batch_size < min_batch_size:
        error_message = f"Requested batch size of {batch_size} is lower that the minimum allowed value of {min_batch_size}"
        with pytest.raises(ValueError, match=error_message):
            _ = create_finetune_request(
                model_limits=_MODEL_LIMITS,
                model=_MODEL_NAME,
                training_file=_TRAINING_FILE,
                batch_size=batch_size,
                lora=use_lora,
            )


def test_non_lora_model():
    with pytest.raises(
        ValueError, match="LoRA adapters are not supported for the selected model."
    ):
        _ = create_finetune_request(
            model_limits=FinetuneTrainingLimits(
                max_num_epochs=20,
                max_learning_rate=1.0,
                min_learning_rate=1e-6,
                full_training=FinetuneFullTrainingLimits(
                    max_batch_size=96,
                    max_batch_size_dpo=48,
                    min_batch_size=8,
                ),
                lora_training=None,
            ),
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            lora=True,
        )


def test_non_full_model():
    with pytest.raises(
        ValueError, match="Full training is not supported for the selected model."
    ):
        _ = create_finetune_request(
            model_limits=FinetuneTrainingLimits(
                max_num_epochs=20,
                max_learning_rate=1.0,
                min_learning_rate=1e-6,
                lora_training=FinetuneLoraTrainingLimits(
                    max_batch_size=96,
                    max_batch_size_dpo=48,
                    min_batch_size=8,
                    max_rank=64,
                    target_modules=["q", "k", "v", "o", "mlp"],
                ),
                full_training=None,
            ),
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            lora=False,
        )


@pytest.mark.parametrize("warmup_ratio", [-1.0, 2.0])
def test_bad_warmup(warmup_ratio):
    with pytest.raises(ValueError, match="Warmup ratio should be between 0 and 1"):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            warmup_ratio=warmup_ratio,
        )


@pytest.mark.parametrize("min_lr_ratio", [-1.0, 2.0])
def test_bad_min_lr_ratio(min_lr_ratio):
    with pytest.raises(
        ValueError, match="Min learning rate ratio should be between 0 and 1"
    ):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            min_lr_ratio=min_lr_ratio,
        )


@pytest.mark.parametrize("max_grad_norm", [-1.0, -0.01])
def test_bad_max_grad_norm(max_grad_norm):
    with pytest.raises(ValueError, match="Max gradient norm should be non-negative"):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            max_grad_norm=max_grad_norm,
        )


@pytest.mark.parametrize("weight_decay", [-1.0, -0.01])
def test_bad_weight_decay(weight_decay):
    with pytest.raises(ValueError, match="Weight decay should be non-negative"):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            weight_decay=weight_decay,
        )


def test_bad_training_method():
    with pytest.raises(ValueError, match="training_method must be one of .*"):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            training_method="NON_SFT",
        )


@pytest.mark.parametrize("train_on_inputs", [True, False, "auto", None])
def test_train_on_inputs_for_sft(train_on_inputs):
    request = create_finetune_request(
        model_limits=_MODEL_LIMITS,
        model=_MODEL_NAME,
        training_file=_TRAINING_FILE,
        training_method="sft",
        train_on_inputs=train_on_inputs,
    )
    assert request.training_method.method == "sft"
    if isinstance(train_on_inputs, bool):
        assert request.training_method.train_on_inputs is train_on_inputs
    else:
        assert request.training_method.train_on_inputs == "auto"


def test_train_on_inputs_not_supported_for_dpo():
    with pytest.raises(
        ValueError, match="train_on_inputs is only supported for SFT training"
    ):
        _ = create_finetune_request(
            model_limits=_MODEL_LIMITS,
            model=_MODEL_NAME,
            training_file=_TRAINING_FILE,
            training_method="dpo",
            train_on_inputs=True,
        )


@patch("together.abstract.api_requestor.APIRequestor.request")
def test_price_estimation_request(mocker):
    test_data = [
        {
            "training_type": "lora",
            "training_method": "sft",
        },
        {
            "training_type": "lora",
            "training_method": "dpo",
        },
        {
            "training_type": "full",
            "training_method": "sft",
        },
    ]
    mocker.return_value = (
        TogetherResponse(
            data={
                "estimated_total_price": 100,
                "allowed_to_proceed": True,
                "estimated_train_token_count": 1000,
                "estimated_eval_token_count": 100,
                "user_limit": 1000,
            },
            headers={},
        ),
        None,
        None,
    )
    client = Together()
    for test_case in test_data:
        response = client.fine_tuning.estimate_price(
            training_file=_TRAINING_FILE,
            model=_MODEL_NAME,
            validation_file=_VALIDATION_FILE,
            n_epochs=1,
            n_evals=0,
            training_type=test_case["training_type"],
            training_method=test_case["training_method"],
        )
        assert response.estimated_total_price > 0
        assert response.allowed_to_proceed
        assert response.estimated_train_token_count > 0
        assert response.estimated_eval_token_count > 0


def test_create_ft_job(mocker):
    mock_requestor = Mock()
    mock_requestor.request = MagicMock()
    mock_requestor.request.side_effect = mock_request
    mocker.patch(
        "together.abstract.api_requestor.APIRequestor", return_value=mock_requestor
    )

    client = Together(api_key="fake_api_key")
    response = client.fine_tuning.create(
        training_file=_TRAINING_FILE,
        model=_MODEL_NAME,
        validation_file=_VALIDATION_FILE,
        n_epochs=1,
        n_evals=0,
        lora=True,
        training_method="sft",
    )

    assert mock_requestor.request.call_count == 3
    assert response.id == "ft-12345678-1234-1234-1234-1234567890ab"

    response = client.fine_tuning.create(
        training_file=_TRAINING_FILE,
        model=None,
        validation_file=_VALIDATION_FILE,
        n_epochs=1,
        n_evals=0,
        lora=True,
        training_method="sft",
        from_checkpoint=_FROM_CHECKPOINT,
    )

    assert mock_requestor.request.call_count == 5
    assert response.id == "ft-12345678-1234-1234-1234-1234567890ab"
