from datetime import datetime
from typing import Any, Dict

import together


def verify_api_key() -> None:
    if together.api_key is None:
        raise together.AuthenticationError(
            "TOGETHER_API_KEY not found. Please set it as an environment variable or set it with together.api_key"
        )


def extract_time(json_obj: Dict[str, Any]) -> int:
    try:
        return int(json_obj["created_at"])
    except KeyError:
        return 0


def parse_timestamp(timestamp: str) -> datetime:
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError("Timestamp does not match any expected format")
