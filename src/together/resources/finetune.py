from typing import Any, Iterator, List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    FinetuneRequest,
    FinetuneResponse,
    TogetherClient,
)


class FineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        training_file: str,
        model: str,
        n_epochs: int = 1,
        n_checkpoints: int | None = 1,
        batch_size: int | None = 32,
        learning_rate: float = 0.00001,
        suffix: str | None = None,
        wandb_api_key: str | None = None,
    ) -> FinetuneResponse:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = FinetuneRequest(
            model=model,
            training_file=training_file,
            n_epochs=n_epochs,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
        ).model_dump()

        response, _, _ = requestor.request(
            method="POST",
            url="/fine-tunes",
            params=parameter_payload,
            stream=False,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        assert isinstance(response, TogetherResponse)
        print(response.data)
        return FinetuneResponse(**response.data)


class AsyncFineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        training_file: str,
        model: str,
        n_epochs: int = 1,
        n_checkpoints: int | None = 1,
        batch_size: int | None = 32,
        learning_rate: float = 0.00001,
        suffix: str | None = None,
        wandb_api_key: str | None = None,
    ) -> FinetuneResponse:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = FinetuneRequest(
            model=model,
            training_file=training_file,
            n_epochs=n_epochs,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
        ).model_dump()

        response, _, _ = requestor.request(
            method="POST",
            url="/fine-tunes",
            params=parameter_payload,
            stream=False,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)
