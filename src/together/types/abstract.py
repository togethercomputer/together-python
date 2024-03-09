from dataclasses import dataclass
from typing import Any, Dict

import pydantic
from pydantic import ConfigDict
from typing_extensions import ClassVar, override

from together.constants import BASE_URL, MAX_CONNECTION_RETRIES, TIMEOUT_SECS


PYDANTIC_V2 = pydantic.VERSION.startswith("2.")


@dataclass
class TogetherClient:
    api_key: str | None = None
    base_url: str | None = BASE_URL
    timeout: float | None = TIMEOUT_SECS
    max_retries: int | None = MAX_CONNECTION_RETRIES
    supplied_headers: Dict[str, str] | None = None


class BaseModel(pydantic.BaseModel):
    if PYDANTIC_V2:
        model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")
    else:

        @property
        @override
        def model_fields_set(self) -> set[str]:
            # a forwards-compat shim for pydantic v2
            return self.__fields_set__

        class Config(pydantic.BaseConfig):  # pyright: ignore[reportDeprecated]
            extra: Any = pydantic.Extra.allow
