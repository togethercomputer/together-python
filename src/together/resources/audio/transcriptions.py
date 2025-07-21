from __future__ import annotations

from pathlib import Path
from typing import Any, BinaryIO, Dict, Optional, Tuple, Union

from together.abstract import api_requestor
from together.types import (
    AudioTimestampGranularities,
    AudioTranscriptionResponse,
    AudioTranscriptionResponseFormat,
    AudioTranscriptionVerboseResponse,
    TogetherClient,
    TogetherRequest,
)


class Transcriptions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create(
        self,
        *,
        file: Union[str, BinaryIO, Path],
        model: str = "openai/whisper-large-v3",
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: Union[str, AudioTranscriptionResponseFormat] = "json",
        temperature: float = 0.0,
        timestamp_granularities: Optional[
            Union[str, AudioTimestampGranularities]
        ] = None,
        **kwargs: Any,
    ) -> Union[AudioTranscriptionResponse, AudioTranscriptionVerboseResponse]:
        """
        Transcribes audio into the input language.

        Args:
            file: The audio file object (not file name) to transcribe, in one of these formats:
                flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.
                Can be a file path (str/Path), file object (BinaryIO), or URL (str).
            model: ID of the model to use. Defaults to "openai/whisper-large-v3".
            language: The language of the input audio. Supplying the input language in
                ISO-639-1 format will improve accuracy and latency.
            prompt: An optional text to guide the model's style or continue a previous
                audio segment. The prompt should match the audio language.
            response_format: The format of the transcript output, in one of these options:
                json, verbose_json.
            temperature: The sampling temperature, between 0 and 1. Higher values like 0.8
                will make the output more random, while lower values like 0.2 will make it
                more focused and deterministic.
            timestamp_granularities: The timestamp granularities to populate for this
                transcription. response_format must be set verbose_json to use timestamp
                granularities. Either or both of these options are supported: word, or segment.

        Returns:
            The transcribed text in the requested format.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # Handle file input - could be a path, URL, or file object
        files_data: Dict[str, Union[Tuple[None, str], BinaryIO]] = {}
        params_data = {}

        if isinstance(file, (str, Path)):
            if isinstance(file, str) and file.startswith(("http://", "https://")):
                # URL string - send as multipart field
                files_data["file"] = (None, file)
            else:
                # Local file path
                file_path = Path(file)
                files_data["file"] = open(file_path, "rb")
        else:
            # File object
            files_data["file"] = file

        # Build request parameters
        params_data.update(
            {
                "model": model,
                "response_format": (
                    response_format.value
                    if hasattr(response_format, "value")
                    else response_format
                ),
                "temperature": temperature,
            }
        )

        if language is not None:
            params_data["language"] = language

        if prompt is not None:
            params_data["prompt"] = prompt

        if timestamp_granularities is not None:
            params_data["timestamp_granularities"] = (
                timestamp_granularities.value
                if hasattr(timestamp_granularities, "value")
                else timestamp_granularities
            )

        # Add any additional kwargs
        params_data.update(kwargs)

        try:
            response, _, _ = requestor.request(
                options=TogetherRequest(
                    method="POST",
                    url="audio/transcriptions",
                    params=params_data,
                    files=files_data,
                ),
            )
        finally:
            # Close file if we opened it
            if files_data and "file" in files_data:
                try:
                    # Only close if it's a file object (not a tuple for URL)
                    file_obj = files_data["file"]
                    if hasattr(file_obj, "close") and not isinstance(file_obj, tuple):
                        file_obj.close()
                except:
                    pass

        # Parse response based on format
        if (
            response_format == "verbose_json"
            or response_format == AudioTranscriptionResponseFormat.VERBOSE_JSON
        ):
            return AudioTranscriptionVerboseResponse(**response.data)
        else:
            return AudioTranscriptionResponse(**response.data)


class AsyncTranscriptions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
        self,
        *,
        file: Union[str, BinaryIO, Path],
        model: str = "openai/whisper-large-v3",
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: Union[str, AudioTranscriptionResponseFormat] = "json",
        temperature: float = 0.0,
        timestamp_granularities: Optional[
            Union[str, AudioTimestampGranularities]
        ] = None,
        **kwargs: Any,
    ) -> Union[AudioTranscriptionResponse, AudioTranscriptionVerboseResponse]:
        """
        Async version of transcribe audio into the input language.

        Args:
            file: The audio file object (not file name) to transcribe, in one of these formats:
                flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm.
                Can be a file path (str/Path), file object (BinaryIO), or URL (str).
            model: ID of the model to use. Defaults to "openai/whisper-large-v3".
            language: The language of the input audio. Supplying the input language in
                ISO-639-1 format will improve accuracy and latency.
            prompt: An optional text to guide the model's style or continue a previous
                audio segment. The prompt should match the audio language.
            response_format: The format of the transcript output, in one of these options:
                json, verbose_json.
            temperature: The sampling temperature, between 0 and 1. Higher values like 0.8
                will make the output more random, while lower values like 0.2 will make it
                more focused and deterministic.
            timestamp_granularities: The timestamp granularities to populate for this
                transcription. response_format must be set verbose_json to use timestamp
                granularities. Either or both of these options are supported: word, or segment.

        Returns:
            The transcribed text in the requested format.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # Handle file input - could be a path, URL, or file object
        files_data: Dict[str, Union[Tuple[None, str], BinaryIO]] = {}
        params_data = {}

        if isinstance(file, (str, Path)):
            if isinstance(file, str) and file.startswith(("http://", "https://")):
                # URL string - send as multipart field
                files_data["file"] = (None, file)
            else:
                # Local file path
                file_path = Path(file)
                files_data["file"] = open(file_path, "rb")
        else:
            # File object
            files_data["file"] = file

        # Build request parameters
        params_data.update(
            {
                "model": model,
                "response_format": (
                    response_format
                    if isinstance(response_format, str)
                    else (
                        response_format.value
                        if hasattr(response_format, "value")
                        else response_format
                    )
                ),
                "temperature": temperature,
            }
        )

        if language is not None:
            params_data["language"] = language

        if prompt is not None:
            params_data["prompt"] = prompt

        if timestamp_granularities is not None:
            params_data["timestamp_granularities"] = (
                timestamp_granularities
                if isinstance(timestamp_granularities, str)
                else (
                    timestamp_granularities.value
                    if hasattr(timestamp_granularities, "value")
                    else timestamp_granularities
                )
            )

        # Add any additional kwargs
        params_data.update(kwargs)

        try:
            response, _, _ = await requestor.arequest(
                options=TogetherRequest(
                    method="POST",
                    url="audio/transcriptions",
                    params=params_data,
                    files=files_data,
                ),
            )
        finally:
            # Close file if we opened it
            if files_data and "file" in files_data:
                try:
                    # Only close if it's a file object (not a tuple for URL)
                    file_obj = files_data["file"]
                    if hasattr(file_obj, "close") and not isinstance(file_obj, tuple):
                        file_obj.close()
                except:
                    pass

        # Parse response based on format
        if (
            response_format == "verbose_json"
            or response_format == AudioTranscriptionResponseFormat.VERBOSE_JSON
        ):
            return AudioTranscriptionVerboseResponse(**response.data)
        else:
            return AudioTranscriptionResponse(**response.data)
