from dataclasses import dataclass
from typing import Dict
from typing_extensions import ClassVar, override

import pydantic
from pydantic import ConfigDict, Field

from together._constants import BASE_URL, MAX_CONNECTION_RETRIES, TIMEOUT_SECS

PYDANTIC_V2 = pydantic.VERSION.startswith("2.")

@dataclass
class TogetherClient:
    api_key: str | None = None
    base_url: str | None = BASE_URL
    timeout: float | None = TIMEOUT_SECS
    max_retries: int | None = MAX_CONNECTION_RETRIES
    default_headers: Dict[str, str] | None = None

class BaseModel(pydantic.BaseModel):
    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")
    else:
        @property
        @override
        def model_fields_set(self) -> set[str]:
            # a forwards-compat shim for pydantic v2
            return self.__fields_set__  # type: ignore

        class Config(pydantic.BaseConfig):  # pyright: ignore[reportDeprecated]
            extra: Any = pydantic.Extra.allow  # type: ignore
