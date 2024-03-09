from __future__ import annotations

from typing import List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    EmbeddingRequest,
    EmbeddingResponse,
    TogetherClient,
)


class Files:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    def list(self) -> EmbeddingResponse:
        response, _, _ = self.requestor.request(
            method="GET",
            url="/files",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)


class AsyncFiles:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    async def create(
        self,
        input: str | List[str],
        model: str,
    ) -> EmbeddingResponse:
        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
        ).model_dump()

        response, _, _ = await self.requestor.arequest(
            method="POST",
            url="/embeddings",
            params=parameter_payload,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)
