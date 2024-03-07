from typing import Any, List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    EmbeddingRequest,
    EmbeddingResponse,
    TogetherClient,
)


class Embeddings:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        input: str | List[str],
        model: str,
    ) -> EmbeddingResponse:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
        ).model_dump()

        response, _, _ = requestor.request(
            method="POST",
            url="/embeddings",
            params=parameter_payload,
            stream=False,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)


class AsyncEmbeddings:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        input: str | List[str],
        model: str,
    ) -> Any:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
        ).model_dump()

        response, _, _ = requestor.request(
            method="POST",
            url="/embeddings",
            params=parameter_payload,
            stream=False,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)
