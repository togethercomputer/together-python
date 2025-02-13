# coding: utf-8

"""
    Together APIs

    The Together REST API. Please see https://docs.together.ai for more details.

    The version of the OpenAPI document: 2.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
    field_validator,
)
from typing import Any, ClassVar, Dict, List, Optional, Union
from together.generated.models.audio_speech_request_model import AudioSpeechRequestModel
from together.generated.models.audio_speech_request_voice import AudioSpeechRequestVoice
from typing import Optional, Set
from typing_extensions import Self


class AudioSpeechRequest(BaseModel):
    """
    AudioSpeechRequest
    """  # noqa: E501

    model: AudioSpeechRequestModel
    input: StrictStr = Field(description="Input text to generate the audio for")
    voice: AudioSpeechRequestVoice
    response_format: Optional[StrictStr] = Field(
        default="wav", description="The format of audio output"
    )
    language: Optional[StrictStr] = Field(
        default="en", description="Language of input text"
    )
    response_encoding: Optional[StrictStr] = Field(
        default="pcm_f32le", description="Audio encoding of response"
    )
    sample_rate: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=44100, description="Sampling rate to use for the output audio"
    )
    stream: Optional[StrictBool] = Field(
        default=False,
        description="If true, output is streamed for several characters at a time instead of waiting for the full response. The stream terminates with `data: [DONE]`. If false, return the encoded audio as octet stream",
    )
    __properties: ClassVar[List[str]] = [
        "model",
        "input",
        "voice",
        "response_format",
        "language",
        "response_encoding",
        "sample_rate",
        "stream",
    ]

    @field_validator("response_format")
    def response_format_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["mp3", "wav", "raw"]):
            raise ValueError("must be one of enum values ('mp3', 'wav', 'raw')")
        return value

    @field_validator("language")
    def language_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(
            [
                "en",
                "de",
                "fr",
                "es",
                "hi",
                "it",
                "ja",
                "ko",
                "nl",
                "pl",
                "pt",
                "ru",
                "sv",
                "tr",
                "zh",
            ]
        ):
            raise ValueError(
                "must be one of enum values ('en', 'de', 'fr', 'es', 'hi', 'it', 'ja', 'ko', 'nl', 'pl', 'pt', 'ru', 'sv', 'tr', 'zh')"
            )
        return value

    @field_validator("response_encoding")
    def response_encoding_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(["pcm_f32le", "pcm_s16le", "pcm_mulaw", "pcm_alaw"]):
            raise ValueError(
                "must be one of enum values ('pcm_f32le', 'pcm_s16le', 'pcm_mulaw', 'pcm_alaw')"
            )
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of AudioSpeechRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of model
        if self.model:
            _dict["model"] = self.model.to_dict()
        # override the default output from pydantic by calling `to_dict()` of voice
        if self.voice:
            _dict["voice"] = self.voice.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AudioSpeechRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "model": (
                    AudioSpeechRequestModel.from_dict(obj["model"])
                    if obj.get("model") is not None
                    else None
                ),
                "input": obj.get("input"),
                "voice": (
                    AudioSpeechRequestVoice.from_dict(obj["voice"])
                    if obj.get("voice") is not None
                    else None
                ),
                "response_format": (
                    obj.get("response_format")
                    if obj.get("response_format") is not None
                    else "wav"
                ),
                "language": (
                    obj.get("language") if obj.get("language") is not None else "en"
                ),
                "response_encoding": (
                    obj.get("response_encoding")
                    if obj.get("response_encoding") is not None
                    else "pcm_f32le"
                ),
                "sample_rate": (
                    obj.get("sample_rate")
                    if obj.get("sample_rate") is not None
                    else 44100
                ),
                "stream": obj.get("stream") if obj.get("stream") is not None else False,
            }
        )
        return _obj
