from typing import Any, Dict, Optional


class TogetherResponse:
    def __init__(self, data: Dict[str, Any], headers: Dict[str, Any]):
        self._headers = headers
        self.data = data

    @property
    def request_id(self) -> str | None:
        if "cf-ray" in self._headers:
            return str(self._headers["cf-ray"])
        return None

    @property
    def requests_remaining(self) -> int | None:
        """
        Number of requests remaining at current rate limit
        """
        if "x-ratelimit-remaining" in self._headers:
            return int(self._headers["x-ratelimit-remaining"])
        return None

    @property
    def processed_by(self) -> str | None:
        if "x-hostname" in self._headers:
            return str(self._headers["x-hostname"])
        return None

    @property
    def response_ms(self) -> int | None:
        if "x-total-time" in self._headers:
            h = self._headers["x-total-time"]
            return None if h is None else round(float(h))
        return None
