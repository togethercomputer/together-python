from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

import pydantic
from pydantic import ConfigDict
from typing_extensions import ClassVar

from together.constants import BASE_URL, MAX_RETRIES, TIMEOUT_SECS

PYDANTIC_V2 = pydantic.VERSION.startswith("2.")


@dataclass
class TogetherClient:
    api_key: str | None = field(default=None, repr=False)
    base_url: str | None = BASE_URL
    timeout: float | None = TIMEOUT_SECS
    max_retries: int | None = MAX_RETRIES
    supplied_headers: Dict[str, str] | None = field(default=None, repr=False)


class BaseModel(pydantic.BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")
