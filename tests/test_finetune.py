import os
import time
from typing import Any, Dict, List, Tuple

import pytest
import requests

import together
from together.utils import parse_timestamp


MODEL = "togethercomputer/llama-2-7b"
N_EPOCHS = 1
N_CHECKPOINTS = 1
BATCH_SIZE = 32
LEARNING_RATE = 0.00001
SUFFIX = "pytest"

CANCEL_TIMEOUT = 60

FT_STATUSES = [
    "pending",
    "queued",
    "running",
    "cancel_requested",
    "cancelled",
    "error",
    "completed",
]


def list_models() -> List[Any]:
    model_list = together.Models.list()
    model: Dict[str, Any]

    finetunable_models = []
    for model in model_list:
        if model.get("finetuning_supported"):
            finetunable_models.append(model.get("name"))
    return finetunable_models


def create_ft(
    model: str,
    n_epochs: int,
    n_checkpoints: int,
    batch_size: int,
    learning_rate: float,
    suffix: str,
) -> Tuple[Dict[Any, Any], str]:
    url = "https://huggingface.co/datasets/laion/OIG/resolve/main/unified_joke_explanations.jsonl"
    save_path = "unified_joke_explanations.jsonl"
    download_response = requests.get(url)

    assert download_response.status_code == 200

    with open(save_path, "wb") as file:
        file.write(download_response.content)

    response = together.Files.upload(save_path)

    os.remove(save_path)

    assert isinstance(response, dict)

    file_id = str(response["id"])

    response = together.Finetune.create(
        training_file=file_id,
        model=model,
        n_epochs=n_epochs,
        n_checkpoints=n_checkpoints,
        batch_size=batch_size,
        learning_rate=learning_rate,
        suffix=suffix,
    )

    return response, file_id


def test_create() -> None:
    response, file_id = create_ft(
        MODEL, N_EPOCHS, N_CHECKPOINTS, BATCH_SIZE, LEARNING_RATE, SUFFIX
    )

    assert isinstance(response, dict)
    assert response["training_file"] == file_id
    assert response["model"] == MODEL
    assert SUFFIX in str(response["model_output_name"])


def test_list() -> None:
    response = together.Finetune.list()
    assert isinstance(response, dict)
    assert isinstance(response["data"], list)


def test_retrieve() -> None:
    ft_list = together.Finetune.list()["data"]
    ft_list.sort(key=lambda x: parse_timestamp(x["created_at"]))
    ft_id = ft_list[-1]["id"]
    response = together.Finetune.retrieve(ft_id)

    assert isinstance(response, dict)
    assert str(response["training_file"]).startswith("file-")
    assert str(response["id"]).startswith("ft-")


def test_list_events() -> None:
    ft_list = together.Finetune.list()["data"]
    ft_list.sort(key=lambda x: parse_timestamp(x["created_at"]))
    ft_id = ft_list[-1]["id"]
    response = together.Finetune.list_events(ft_id)

    assert isinstance(response, dict)
    assert isinstance(response["data"], list)


def test_status() -> None:
    ft_list = together.Finetune.list()["data"]
    ft_list.sort(key=lambda x: parse_timestamp(x["created_at"]))
    ft_id = ft_list[-1]["id"]
    response = together.Finetune.get_job_status(ft_id)

    assert isinstance(response, str)
    assert response in FT_STATUSES


def test_download() -> None:
    ft_list = together.Finetune.list()["data"]
    ft_list.sort(key=lambda x: parse_timestamp(x["created_at"]))
    ft_list.reverse()

    ft_id = None
    for item in ft_list:
        id = item["id"]
        if together.Finetune.get_job_status(id) == "completed":
            ft_id = id
            break

    if ft_id is None:
        # no models available to download
        assert False

    output_file = together.Finetune.download(ft_id)

    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0

    os.remove(output_file)


def test_cancel() -> None:
    cancelled = False

    response, file_id = create_ft(
        MODEL, N_EPOCHS, N_CHECKPOINTS, BATCH_SIZE, LEARNING_RATE, SUFFIX
    )
    ft_id = response["id"]
    response = together.Finetune.cancel(ft_id)

    # loop to check if job was cancelled
    start = time.time()
    while time.time() - start < CANCEL_TIMEOUT:
        status = together.Finetune.get_job_status(ft_id)
        if status == "cancel_requested":
            cancelled = True
            break
        time.sleep(1)

    assert cancelled

    # delete file after cancelling
    together.Files.delete(file_id)


def test_checkpoints() -> None:
    ft_list = together.Finetune.list()["data"]
    ft_list.sort(key=lambda x: parse_timestamp(x["created_at"]))
    ft_list.reverse()

    ft_id = None
    for item in ft_list:
        id = item["id"]
        if together.Finetune.get_job_status(id) == "completed":
            ft_id = id
            break

    if ft_id is None:
        # no models available to download
        assert False

    response = together.Finetune.get_checkpoints(ft_id)

    assert isinstance(response, list)


if __name__ == "__main__":
    assert (
        together.api_key
    ), "No API key found, please run `export TOGETHER_API_KEY=<API_KEY>`"
    pytest.main([__file__])
