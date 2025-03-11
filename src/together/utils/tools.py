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
    """Parse a timestamp string into a datetime object or None if the string is empty.

    Args:
        timestamp (str): Timestamp

    Returns:
        datetime | None: Parsed datetime, or None if the string is empty
    """
    if timestamp == "":
        return None

    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue

    raise ValueError("Timestamp does not match any expected format")


def format_timestamp(timestamp_str: str) -> str:
    """Format timestamp to a readable date string.

    Args:
        timestamp: A timestamp string

    Returns:
        str: Formatted timestamp string (MM/DD/YYYY, HH:MM AM/PM)
    """
    timestamp = parse_timestamp(timestamp_str)
    if timestamp is None:
        return ""
    return timestamp.strftime("%m/%d/%Y, %I:%M %p")


def get_event_step(event: Any) -> str | None:
    """Extract the step number from a checkpoint event.

    Args:
        event: A checkpoint event object

    Returns:
        str | None: The step number as a string, or None if not found
    """
    step = getattr(event, "step", None)
    if step is not None:
        return str(step)
    return None


def finetune_price_to_dollars(price: float) -> float:
    """Convert fine-tuning job price to dollars

    Args:
        price (float): Fine-tuning job price in billing units

    Returns:
        float: Price in dollars
    """
    return price / NANODOLLAR


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
