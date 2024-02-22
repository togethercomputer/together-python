from dataclasses import dataclass
from typing import Dict

from together._constants import BASE_URL, MAX_CONNECTION_RETRIES, TIMEOUT_SECS


@dataclass
class TogetherClient:
    api_key: str | None = None
    base_url: str | None = BASE_URL
    timeout: float | None = TIMEOUT_SECS
    max_retries: int | None = MAX_CONNECTION_RETRIES
    default_headers: Dict[str, str] | None = None
