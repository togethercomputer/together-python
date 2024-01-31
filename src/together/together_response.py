from typing import Optional


class TogetherResponse:
    def __init__(self, data, headers):
        self._headers = headers
        self.data = data

    @property
    def request_id(self) -> Optional[str]:
        return self._headers.get("cf-ray")

    @property
    def requests_remaining(self) -> Optional[int]:
        """
        Number of requests remaining at current rate limit
        """
        try:
            return int(self._headers.get("x-ratelimit-remaining"))
        except TypeError:
            return None

    @property
    def processed_by(self) -> Optional[str]:
        return self._headers.get("x-hostname")

    @property
    def response_ms(self) -> Optional[int]:
        h = self._headers.get("x-total-time")
        return None if h is None else round(float(h))
