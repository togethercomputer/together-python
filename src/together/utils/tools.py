from __future__ import annotations

import logging
import os
from datetime import datetime
import re
from typing import Any


logger = logging.getLogger("together")

TOGETHER_LOG = os.environ.get("TOGETHER_LOG")

NANODOLLAR = 1_000_000_000


def enforce_trailing_slash(url: str) -> str:
    if not url.endswith("/"):
        return url + "/"
    else:
        return url


def normalize_key(key: str) -> str:
    return key.replace("/", "--").replace("_", "-").replace(" ", "-").lower()


def parse_timestamp(timestamp: str) -> datetime | None:
    """Parse a timestamp string into a datetime object or None if invalid.

    Args:
        timestamp (str): Timestamp in ISO 8601 format (e.g. "2021-01-01T00:00:00Z")

    Returns:
        datetime | None: Parsed datetime, or None if the string is empty
    """
    if timestamp == "":
        return None

    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def format_event_timestamp(event: Any) -> str:
    """Format event timestamp to a readable date string.

    Args:
        event: An event object with a created_at attribute

    Returns:
        str: Formatted timestamp string (MM/DD/YYYY, HH:MM AM/PM)
    """
    timestamp = parse_timestamp(event.created_at or "")
    return timestamp.strftime("%m/%d/%Y, %I:%M %p") if timestamp else ""


def get_event_step(event: Any) -> str | None:
    """Extract the step number from a checkpoint event.

    Args:
        event: A checkpoint event object

    Returns:
        str | None: The step number as a string, or None if not found
    """
    # First try to get step directly from the event object
    step = getattr(event, "step", None)
    if step is not None:
        return str(step)

    # If not available, try to extract from the message
    message = getattr(event, "message", "") or ""
    step_match = re.search(r"step[:\s]+(\d+)", message.lower())
    return step_match.group(1) if step_match else None


# Convert fine-tune nano-dollar price to dollars
def finetune_price_to_dollars(price: float) -> float:
    """Convert fine-tune price to dollars

    Args:
        price (float): Fine-tune price in billing units

    Returns:
        float: Price in dollars
    """
    # Convert from nanodollars (1e-9 dollars) to dollars
    return price / 1e9


def convert_bytes(num: float) -> str | None:
    """
    Convert bytes to a human-readable format.

    Args:
        num (int): Number of bytes.

    Returns:
        str: Human-readable representation of the size.
    """
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if num < 1024.0:
            return "{:.1f} {}".format(num, unit)
        num /= 1024.0

    return None


def convert_unix_timestamp(timestamp: int) -> str:
    """
    Convert a Unix timestamp to a human-readable date and time format.

    Args:
        timestamp (int): Unix timestamp.

    Returns:
        str: Human-readable date and time string.
    """
    # Convert Unix timestamp to datetime object
    dt_object = datetime.fromtimestamp(timestamp)

    # Format datetime object as ISO 8601 string
    iso_format = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return iso_format
