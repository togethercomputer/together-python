from typing import List

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
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    def create(
        self,
        input: str | List[str],
        model: str,
    ) -> EmbeddingResponse:
        parameter_payload = EmbeddingRequest(
            input=input,
            model=model,
        ).model_dump()

        response, _, _ = self.requestor.request(
            method="POST",
            url="/embeddings",
            params=parameter_payload,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return EmbeddingResponse(**response.data)


class AsyncEmbeddings:
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
