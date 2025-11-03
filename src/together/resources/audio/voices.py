from __future__ import annotations

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    TogetherClient,
    TogetherRequest,
    VoiceListResponse,
)


class Voices:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def list(self) -> VoiceListResponse:
        """
        Method to return list of available voices on the API

        Returns:
            VoiceListResponse: Response containing models and their available voices
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="voices",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return VoiceListResponse(**response.data)


class AsyncVoices:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def list(self) -> VoiceListResponse:
        """
        Async method to return list of available voices on the API

        Returns:
            VoiceListResponse: Response containing models and their available voices
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="voices",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return VoiceListResponse(**response.data)
