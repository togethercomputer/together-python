from functools import cached_property

from together.resources.audio.speech import AsyncSpeech, Speech
from together.types import (
    TogetherClient,
)


class Audio:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @cached_property
    def speech(self) -> Speech:
        return Speech(self._client)


class AsyncAudio:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @cached_property
    def speech(self) -> AsyncSpeech:
        return AsyncSpeech(self._client)
