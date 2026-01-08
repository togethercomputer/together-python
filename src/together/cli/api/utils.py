from __future__ import annotations

import math
import re
from gettext import gettext as _
from typing import Literal
from datetime import datetime

import click

from together.types.finetune import FinetuneResponse, COMPLETED_STATUSES

_PROGRESS_BAR_WIDTH = 40


class AutoIntParamType(click.ParamType):
    name = "integer_or_max"
    _number_class = int

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> int | Literal["max"] | None:
        if value == "max":
            return "max"
        try:
            return int(value)
        except ValueError:
            self.fail(
                _("{value!r} is not a valid {number_type}.").format(
                    value=value, number_type=self.name
                ),
                param,
                ctx,
            )


class BooleanWithAutoParamType(click.ParamType):
    name = "boolean_or_auto"

    def convert(
        self, value: str, param: click.Parameter | None, ctx: click.Context | None
    ) -> bool | Literal["auto"] | None:
        if value == "auto":
            return "auto"
        try:
            return bool(value)
        except ValueError:
            self.fail(
                _("{value!r} is not a valid {type}.").format(
                    value=value, type=self.name
                ),
                param,
                ctx,
            )


INT_WITH_MAX = AutoIntParamType()
BOOL_WITH_AUTO = BooleanWithAutoParamType()


def _human_readable_time(timedelta: float) -> str:
    """Convert a timedelta to a compact human-readble string
    Examples:
        00:00:10 -> 10s
        01:23:45 -> 1h 23min 45s
        1 Month 23 days 04:56:07 -> 1month 23d 4h 56min 7s
    Args:
        timedelta (float): The timedelta in seconds to convert.
    Returns:
        A string representing the timedelta in a human-readable format.
    """
    units = [
        (30 * 24 * 60 * 60, "month"),  # 30 days
        (24 * 60 * 60, "d"),
        (60 * 60, "h"),
        (60, "min"),
        (1, "s"),
    ]

    total_seconds = int(timedelta)
    parts = []

    for unit_seconds, unit_name in units:
        if total_seconds >= unit_seconds:
            value = total_seconds // unit_seconds
            total_seconds %= unit_seconds
            parts.append(f"{value}{unit_name}")

    return " ".join(parts) if parts else "0s"


def generate_progress_bar(
    finetune_job: FinetuneResponse, current_time: datetime, use_rich: bool = False
) -> str:
    """Generate a progress bar for a finetune job.
    Args:
        finetune_job: The finetune job to generate a progress bar for.
        current_time: The current time.
        use_rich: Whether to use rich formatting.
    Returns:
        A string representing the progress bar.
    """
    progress = "Progress: [bold red]unavailable[/bold red]"
    if finetune_job.status in COMPLETED_STATUSES:
        progress = "Progress: [bold green]completed[/bold green]"
    elif finetune_job.started_at is not None:
        # Replace 'Z' with '+00:00' for Python 3.10 compatibility
        started_at_str = finetune_job.started_at.replace("Z", "+00:00")
        started_at = datetime.fromisoformat(started_at_str).astimezone()

        if finetune_job.progress is not None:
            if current_time < started_at:
                return progress

            if not finetune_job.progress.estimate_available:
                return progress

            if finetune_job.progress.seconds_remaining <= 0:
                return progress

            elapsed_time = (current_time - started_at).total_seconds()
            ratio_filled = min(
                elapsed_time / finetune_job.progress.seconds_remaining, 1.0
            )
            percentage = ratio_filled * 100
            filled = math.ceil(ratio_filled * _PROGRESS_BAR_WIDTH)
            bar = "█" * filled + "░" * (_PROGRESS_BAR_WIDTH - filled)
            time_left = "N/A"
            if finetune_job.progress.seconds_remaining > elapsed_time:
                time_left = _human_readable_time(
                    finetune_job.progress.seconds_remaining - elapsed_time
                )
            time_text = f"{time_left} left"
            progress = f"Progress: {bar} [bold]{percentage:>3.0f}%[/bold] [yellow]{time_text}[/yellow]"

    if use_rich:
        return progress

    return re.sub(r"\[/?[^\]]+\]", "", progress)
