from __future__ import annotations

import base64
from enum import Enum
from re import S
from typing import BinaryIO, Dict, Iterator, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from together.together_response import TogetherResponse


class AudioResponseFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    RAW = "raw"


class AudioLanguage(str, Enum):
    EN = "en"
    DE = "de"
    FR = "fr"
    ES = "es"
    HI = "hi"
    IT = "it"
    JA = "ja"
    KO = "ko"
    NL = "nl"
    PL = "pl"
    PT = "pt"
    RU = "ru"
    SV = "sv"
    TR = "tr"
    ZH = "zh"


class AudioResponseEncoding(str, Enum):
    PCM_F32LE = "pcm_f32le"
    PCM_S16LE = "pcm_s16le"
    PCM_MULAW = "pcm_mulaw"
    PCM_ALAW = "pcm_alaw"


class AudioObjectType(str, Enum):
    AUDIO_TTS_CHUNK = "audio.tts.chunk"


class StreamSentinelType(str, Enum):
    DONE = "[DONE]"


class AudioSpeechRequest(BaseModel):
    model: str
    input: str
    voice: str | None = None
    response_format: AudioResponseFormat = AudioResponseFormat.MP3
    language: AudioLanguage = AudioLanguage.EN
    response_encoding: AudioResponseEncoding = AudioResponseEncoding.PCM_F32LE
    sample_rate: int = 44100
    stream: bool = False


class AudioSpeechStreamChunk(BaseModel):
    object: AudioObjectType = AudioObjectType.AUDIO_TTS_CHUNK
    model: str
    b64: str


class AudioSpeechStreamEvent(BaseModel):
    data: AudioSpeechStreamChunk


class StreamSentinel(BaseModel):
    data: StreamSentinelType = StreamSentinelType.DONE


class AudioSpeechStreamEventResponse(BaseModel):
    response: AudioSpeechStreamEvent | StreamSentinel


class AudioSpeechStreamResponse(BaseModel):
    response: TogetherResponse | Iterator[TogetherResponse]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def stream_to_file(
        self, file_path: str, response_format: AudioResponseFormat | str | None = None
    ) -> None:
        """
        Save the audio response to a file.

        For non-streaming responses, writes the complete file as received.
        For streaming responses, collects binary chunks and constructs a valid
        file format based on the response_format parameter.

        Args:
            file_path: Path where the audio file should be saved.
            response_format: Format of the audio (wav, mp3, or raw). If not provided,
                           will attempt to infer from file extension or default to wav.
        """
        # Determine response format
        if response_format is None:
            # Infer from file extension
            ext = file_path.lower().split(".")[-1] if "." in file_path else ""
            if ext in ["wav"]:
                response_format = AudioResponseFormat.WAV
            elif ext in ["mp3", "mpeg"]:
                response_format = AudioResponseFormat.MP3
            elif ext in ["raw", "pcm"]:
                response_format = AudioResponseFormat.RAW
            else:
                # Default to WAV if unknown
                response_format = AudioResponseFormat.WAV

        if isinstance(response_format, str):
            response_format = AudioResponseFormat(response_format)

        if isinstance(self.response, TogetherResponse):
            # Non-streaming: save complete file
            with open(file_path, "wb") as f:
                f.write(self.response.data)

        elif isinstance(self.response, Iterator):
            # Streaming: collect binary chunks
            audio_chunks = []
            for chunk in self.response:
                if isinstance(chunk.data, bytes):
                    audio_chunks.append(chunk.data)
                elif isinstance(chunk.data, dict):
                    # SSE format with JSON/base64
                    try:
                        stream_event = AudioSpeechStreamEventResponse(
                            response={"data": chunk.data}
                        )
                        if isinstance(stream_event.response, StreamSentinel):
                            break
                        audio_chunks.append(
                            base64.b64decode(stream_event.response.data.b64)
                        )
                    except Exception:
                        continue  # Skip malformed chunks

            if not audio_chunks:
                raise ValueError("No audio data received in streaming response")

            # Concatenate all chunks
            audio_data = b"".join(audio_chunks)

            with open(file_path, "wb") as f:
                if response_format == AudioResponseFormat.WAV:
                    if audio_data.startswith(b"RIFF"):
                        # Already a valid WAV file
                        f.write(audio_data)
                    else:
                        # Raw PCM - add WAV header
                        self._write_wav_header(f, audio_data)
                elif response_format == AudioResponseFormat.MP3:
                    # MP3 format: Check if data is actually MP3 or raw PCM
                    # MP3 files start with ID3 tag or sync word (0xFF 0xFB/0xFA/0xF3/0xF2)
                    is_mp3 = audio_data.startswith(b"ID3") or (
                        len(audio_data) > 0
                        and audio_data[0:1] == b"\xff"
                        and len(audio_data) > 1
                        and audio_data[1] & 0xE0 == 0xE0
                    )

                    if is_mp3:
                        f.write(audio_data)
                    else:
                        raise ValueError("Invalid MP3 data received.")
                else:
                    # RAW format: write PCM data as-is
                    f.write(audio_data)

    @staticmethod
    def _write_wav_header(file_handle: BinaryIO, audio_data: bytes) -> None:
        """
        Write WAV file header for raw PCM audio data.

        Uses default TTS parameters: 16-bit PCM, mono, 24000 Hz sample rate.
        """
        import struct

        sample_rate = 24000
        num_channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        data_size = len(audio_data)

        # Write WAV header
        file_handle.write(b"RIFF")
        file_handle.write(struct.pack("<I", 36 + data_size))  # File size - 8
        file_handle.write(b"WAVE")
        file_handle.write(b"fmt ")
        file_handle.write(struct.pack("<I", 16))  # fmt chunk size
        file_handle.write(struct.pack("<H", 1))  # Audio format (1 = PCM)
        file_handle.write(struct.pack("<H", num_channels))
        file_handle.write(struct.pack("<I", sample_rate))
        file_handle.write(struct.pack("<I", byte_rate))
        file_handle.write(struct.pack("<H", block_align))
        file_handle.write(struct.pack("<H", bits_per_sample))
        file_handle.write(b"data")
        file_handle.write(struct.pack("<I", data_size))
        file_handle.write(audio_data)


class AudioTranscriptionResponseFormat(str, Enum):
    JSON = "json"
    VERBOSE_JSON = "verbose_json"


class AudioTimestampGranularities(str, Enum):
    SEGMENT = "segment"
    WORD = "word"


class AudioTranscriptionRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: Union[str, BinaryIO]
    model: str = "openai/whisper-large-v3"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: AudioTranscriptionResponseFormat = (
        AudioTranscriptionResponseFormat.JSON
    )
    temperature: float = 0.0
    timestamp_granularities: Optional[AudioTimestampGranularities] = (
        AudioTimestampGranularities.SEGMENT
    )


class AudioTranslationRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    file: Union[str, BinaryIO]
    model: str = "openai/whisper-large-v3"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: AudioTranscriptionResponseFormat = (
        AudioTranscriptionResponseFormat.JSON
    )
    temperature: float = 0.0
    timestamp_granularities: Optional[AudioTimestampGranularities] = (
        AudioTimestampGranularities.SEGMENT
    )


class AudioTranscriptionSegment(BaseModel):
    id: int
    start: float
    end: float
    text: str


class AudioTranscriptionWord(BaseModel):
    word: str
    start: float
    end: float
    id: Optional[int] = None
    speaker_id: Optional[str] = None


class AudioSpeakerSegment(BaseModel):
    id: int
    speaker_id: str
    start: float
    end: float
    text: str
    words: List[AudioTranscriptionWord]


class AudioTranscriptionResponse(BaseModel):
    text: str


class AudioTranscriptionVerboseResponse(BaseModel):
    id: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[float] = None
    text: str
    segments: Optional[List[AudioTranscriptionSegment]] = None
    words: Optional[List[AudioTranscriptionWord]] = None
    speaker_segments: Optional[List[AudioSpeakerSegment]] = None


class AudioTranslationResponse(BaseModel):
    text: str


class AudioTranslationVerboseResponse(BaseModel):
    task: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[float] = None
    text: str
    segments: Optional[List[AudioTranscriptionSegment]] = None
    words: Optional[List[AudioTranscriptionWord]] = None


class ModelVoices(BaseModel):
    """Represents a model with its available voices."""

    model: str
    voices: List[Dict[str, str]]  # Each voice is a dict with 'name' key


class VoiceListResponse(BaseModel):
    """Response containing a list of models and their available voices."""

    data: List[ModelVoices]
