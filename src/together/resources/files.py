from __future__ import annotations

from typing import List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    EmbeddingRequest,
    EmbeddingResponse,
    TogetherClient,
    TogetherRequest,
)


class Files:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def list(self) -> EmbeddingResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="/files",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)


class AsyncFiles:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        input: str | List[str],
        model: str,
    ) -> EmbeddingResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
        ).model_dump()

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="/embeddings",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)
