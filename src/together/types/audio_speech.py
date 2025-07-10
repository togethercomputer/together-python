from __future__ import annotations

import base64
from enum import Enum
from typing import BinaryIO, Iterator, List, Optional, Union

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

    def stream_to_file(self, file_path: str) -> None:
        if isinstance(self.response, TogetherResponse):
            # save response to file
            with open(file_path, "wb") as f:
                f.write(self.response.data)

        elif isinstance(self.response, Iterator):
            with open(file_path, "wb") as f:
                for chunk in self.response:
                    # Try to parse as stream chunk
                    stream_event_response = AudioSpeechStreamEventResponse(
                        response={"data": chunk.data}
                    )

                    if isinstance(stream_event_response.response, StreamSentinel):
                        break

                    # decode base64
                    audio = base64.b64decode(stream_event_response.response.data.b64)

                    f.write(audio)


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


class AudioTranscriptionResponse(BaseModel):
    text: str


class AudioTranscriptionVerboseResponse(BaseModel):
    language: Optional[str] = None
    duration: Optional[float] = None
    text: str
    segments: Optional[List[AudioTranscriptionSegment]] = None
    words: Optional[List[AudioTranscriptionWord]] = None


class AudioTranslationResponse(BaseModel):
    text: str


class AudioTranslationVerboseResponse(BaseModel):
    task: Optional[str] = None
    language: Optional[str] = None
    duration: Optional[float] = None
    text: str
    segments: Optional[List[AudioTranscriptionSegment]] = None
    words: Optional[List[AudioTranscriptionWord]] = None
