from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, Iterator, List, Union

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    AudioSpeechRequest,
    AudioResponseFormat,
    AudioLanguage,
    AudioResponseEncoding,
    AudioSpeechStreamChunk,
    AudioSpeechStreamEvent,
    AudioSpeechStreamResponse,
    TogetherClient,
    TogetherRequest,
)


class Speech:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        input: str,
        voice: str | None = None,
        response_format: str = "wav",
        language: str = "en",
        response_encoding: str = "pcm_f32le",
        sample_rate: int = 44100,
        stream: bool = False,
        **kwargs: Any,
    ) -> AudioSpeechStreamResponse:
        """
        Method to generate audio from input text using a specified model.

        Args:
            model (str): The name of the model to query.
            input (str): Input text to generate the audio for.
            voice (str, optional): The voice to use for generating the audio.
                Defaults to None.
            response_format (str, optional): The format of audio output.
                Defaults to "wav".
            language (str, optional): Language of input text.
                Defaults to "en".
            response_encoding (str, optional): Audio encoding of response.
                Defaults to "pcm_f32le".
            sample_rate (int, optional): Sampling rate to use for the output audio.
                Defaults to 44100.
            stream (bool, optional): If true, output is streamed for several characters at a time.
                Defaults to False.

        Returns:
            Union[bytes, Iterator[AudioSpeechStreamChunk]]: The generated audio as bytes or an iterator over audio stream chunks.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AudioSpeechRequest(
            model=model,
            input=input,
            voice=voice,
            response_format=AudioResponseFormat(response_format),
            language=AudioLanguage(language),
            response_encoding=AudioResponseEncoding(response_encoding),
            sample_rate=sample_rate,
            stream=stream,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, streamed, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="audio/speech",
                params=parameter_payload,
            ),
            stream=stream,
        )

        return AudioSpeechStreamResponse(response=response)


class AsyncSpeech:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        model: str,
        input: str,
        voice: str | None = None,
        response_format: str = "wav",
        language: str = "en",
        response_encoding: str = "pcm_f32le",
        sample_rate: int = 44100,
        stream: bool = False,
        **kwargs: Any,
    ) -> AudioSpeechStreamResponse:
        """
        Async method to generate audio from input text using a specified model.

        Args:
            model (str): The name of the model to query.
            input (str): Input text to generate the audio for.
            voice (str, optional): The voice to use for generating the audio.
                Defaults to None.
            response_format (str, optional): The format of audio output.
                Defaults to "wav".
            language (str, optional): Language of input text.
                Defaults to "en".
            response_encoding (str, optional): Audio encoding of response.
                Defaults to "pcm_f32le".
            sample_rate (int, optional): Sampling rate to use for the output audio.
                Defaults to 44100.
            stream (bool, optional): If true, output is streamed for several characters at a time.
                Defaults to False.

        Returns:
            Union[bytes, AsyncGenerator[AudioSpeechStreamChunk, None]]: The generated audio as bytes or an async generator over audio stream chunks.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = AudioSpeechRequest(
            model=model,
            input=input,
            voice=voice,
            response_format=AudioResponseFormat(response_format),
            language=AudioLanguage(language),
            response_encoding=AudioResponseEncoding(response_encoding),
            sample_rate=sample_rate,
            stream=stream,
            **kwargs,
        ).model_dump(exclude_none=True)

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="audio/speech",
                params=parameter_payload,
            ),
            stream=stream,
        )

        return AudioSpeechStreamResponse(response=response)
