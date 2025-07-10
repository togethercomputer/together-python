from functools import cached_property

from together.resources.audio.speech import AsyncSpeech, Speech
from together.resources.audio.transcriptions import AsyncTranscriptions, Transcriptions
from together.resources.audio.translations import AsyncTranslations, Translations
from together.types import (
    TogetherClient,
)


class Audio:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @cached_property
    def speech(self) -> Speech:
        return Speech(self._client)

    @cached_property
    def transcriptions(self) -> Transcriptions:
        return Transcriptions(self._client)

    @cached_property
    def translations(self) -> Translations:
        return Translations(self._client)


class AsyncAudio:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @cached_property
    def speech(self) -> AsyncSpeech:
        return AsyncSpeech(self._client)

    @cached_property
    def transcriptions(self) -> AsyncTranscriptions:
        return AsyncTranscriptions(self._client)

    @cached_property
    def translations(self) -> AsyncTranslations:
        return AsyncTranslations(self._client)
