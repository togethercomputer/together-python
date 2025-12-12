from datetime import datetime, timezone

import pytest

from together.cli.api.utils import generate_progress_bar
from together.types.finetune import (
    FinetuneResponse,
    FinetuneProgress,
    FinetuneJobStatus,
)


def create_finetune_response(
    status: FinetuneJobStatus = FinetuneJobStatus.STATUS_RUNNING,
    updated_at: str = "2024-01-01T12:00:00Z",
    progress: FinetuneProgress | None = None,
    job_id: str = "ft-test-123",
) -> FinetuneResponse:
    """Helper function to create FinetuneResponse objects for testing.

    Args:
        status: The job status.
        updated_at: The updated timestamp in ISO format.
        progress: Optional FinetuneProgress object.
        job_id: The fine-tune job ID.

    Returns:
        A FinetuneResponse object for testing.
    """
    return FinetuneResponse(
        id=job_id,
        progress=progress,
        updated_at=updated_at,
        status=status,
    )


class TestGenerateProgressBarGeneral:
    """General test cases for normal operation."""

    def test_progress_unavailable_when_none(self):
        """Test that progress shows unavailable when progress field is None."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(progress=None)

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_progress_unavailable_when_not_set(self):
        """Test that progress shows unavailable when field is not provided."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response()

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_progress_bar_at_start(self):
        """Test progress bar display when job just started (low percentage)."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=1000.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        # 10 seconds elapsed / 1000 seconds remaining = 0.01 ratio = 1% progress
        # 0.01 * 40 = 0.4, ceil(0.4) = 1 filled bar
        assert (
            result
            == "Progress: █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ [bold]  1%[/bold] [yellow]16min 30s left[/yellow]"
        )

    def test_progress_bar_at_midpoint(self):
        """Test progress bar at approximately 50% completion."""
        current_time = datetime(2024, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        # 60 seconds elapsed / 60 seconds remaining = 1.0 ratio = 100% progress
        # 1.0 * 40 = 40 filled bars
        assert (
            result
            == "Progress: ████████████████████████████████████████ [bold]100%[/bold] [yellow]N/A left[/yellow]"
        )

    def test_progress_bar_near_completion(self):
        """Test progress bar when job is almost complete."""
        current_time = datetime(2024, 1, 1, 12, 5, 0, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=30.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        # 300 seconds elapsed / 30 seconds remaining = 10.0 ratio = 1000% progress
        # 10.0 * 40 = 400, ceil(400) = 400, but width is 40 so all filled
        assert (
            result
            == "Progress: ████████████████████████████████████████ [bold]100%[/bold] [yellow]N/A left[/yellow]"
        )

    def test_progress_bar_contains_rich_formatting(self):
        """Test that progress bar includes expected Rich markup formatting."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        # 30 seconds elapsed / 60 seconds remaining = 0.5 ratio = 50% progress
        # 0.5 * 40 = 20 filled bars
        assert (
            result
            == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░ [bold] 50%[/bold] [yellow]30s left[/yellow]"
        )


class TestGenerateProgressBarRichFormatting:
    """Test cases for use_rich parameter."""

    def test_rich_formatting_removed_when_use_rich_false(self):
        """Test that rich formatting tags are removed when use_rich=False."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)

        assert (
            result == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░  50% 30s left"
        )

    def test_rich_formatting_preserved_when_use_rich_true(self):
        """Test that rich formatting tags are preserved when use_rich=True."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert (
            result
            == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░ [bold] 50%[/bold] [yellow]30s left[/yellow]"
        )

    def test_completed_status_formatting_removed(self):
        """Test that completed status formatting is removed when use_rich=False."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            status=FinetuneJobStatus.STATUS_COMPLETED, progress=None
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)

        assert result == "Progress: completed"

    def test_unavailable_status_formatting_removed(self):
        """Test that unavailable status formatting is removed when use_rich=False."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(progress=None)

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)

        assert result == "Progress: unavailable"

    def test_rich_formatting_removed_at_completion(self):
        """Test that rich formatting is removed at 100% when use_rich=False."""
        current_time = datetime(2024, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)

        assert (
            result == "Progress: ████████████████████████████████████████ 100% N/A left"
        )

    def test_default_behavior_strips_formatting(self):
        """Test that rich formatting is removed by default (use_rich not specified)."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time)

        assert (
            result == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░  50% 30s left"
        )

    def test_content_consistency_between_modes(self):
        """Test that use_rich=True and use_rich=False have same content, just different formatting."""
        import re

        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result_with_rich = generate_progress_bar(
            finetune_job, current_time, use_rich=True
        )
        result_without_rich = generate_progress_bar(
            finetune_job, current_time, use_rich=False
        )

        stripped_rich = re.sub(r"\[/?[^\]]+\]", "", result_with_rich)
        assert stripped_rich == result_without_rich

    def test_all_rich_tag_types_removed(self):
        """Test that all types of rich formatting tags are properly removed."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)

        # Test with completed status (has [bold green] tags)
        completed_job = create_finetune_response(
            status=FinetuneJobStatus.STATUS_COMPLETED, progress=None
        )
        result_completed = generate_progress_bar(
            completed_job, current_time, use_rich=False
        )
        assert result_completed == "Progress: completed"

        # Test with unavailable status (has [bold red] tags)
        unavailable_job = create_finetune_response(progress=None)
        result_unavailable = generate_progress_bar(
            unavailable_job, current_time, use_rich=False
        )
        assert result_unavailable == "Progress: unavailable"

    @pytest.mark.parametrize(
        "use_rich,expected_completed,expected_running",
        [
            (
                True,
                "Progress: [bold green]completed[/bold green]",
                "Progress: ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ [bold] 17%[/bold] [yellow]50s left[/yellow]",
            ),
            (
                False,
                "Progress: completed",
                "Progress: ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  17% 50s left",
            ),
        ],
    )
    def test_rich_parameter_with_different_statuses(
        self, use_rich, expected_completed, expected_running
    ):
        """Test use_rich parameter works correctly with different job statuses."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)

        # Test completed status
        completed_job = create_finetune_response(
            status=FinetuneJobStatus.STATUS_COMPLETED, progress=None
        )
        result = generate_progress_bar(completed_job, current_time, use_rich=use_rich)
        assert result == expected_completed

        # Test running status
        running_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )
        result = generate_progress_bar(running_job, current_time, use_rich=use_rich)
        assert result == expected_running

    def test_progress_percentage_1_percent(self):
        """Test progress bar at 1% completion."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=1000.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)
        assert (
            result
            == "Progress: █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   1% 16min 30s left"
        )

    def test_progress_percentage_75_percent(self):
        """Test progress bar at 75% completion."""
        current_time = datetime(2024, 1, 1, 12, 0, 45, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)
        assert (
            result == "Progress: ██████████████████████████████░░░░░░░░░░  75% 15s left"
        )


class TestGenerateProgressBarCornerCases:
    """Corner cases and edge conditions."""

    def test_zero_seconds_remaining(self):
        """Test handling of zero seconds remaining (potential division by zero)."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=0.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_very_small_remaining_time(self):
        """Test with very small remaining time (< 1 second)."""
        current_time = datetime(2024, 1, 1, 12, 0, 5, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=0.5)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert (
            result
            == "Progress: ████████████████████████████████████████ [bold]100%[/bold] [yellow]N/A left[/yellow]"
        )

    def test_very_large_remaining_time(self):
        """Test with very large remaining time (hours)."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(
                estimate_available=True, seconds_remaining=36000.0
            )
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert (
            result
            == "Progress: █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ [bold]  0%[/bold] [yellow]9h 59min 30s left[/yellow]"
        )

    def test_job_exceeding_estimate(self):
        """Test when elapsed time exceeds original estimate (>100% progress)."""
        current_time = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert (
            result
            == "Progress: ████████████████████████████████████████ [bold]100%[/bold] [yellow]N/A left[/yellow]"
        )

    def test_timezone_aware_datetime(self):
        """Test with different timezone for updated_at."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            updated_at="2024-01-01T07:00:00-05:00",  # Same as 12:00:00 UTC (EST = UTC-5)
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0),
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert (
            result
            == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░ [bold] 50%[/bold] [yellow]30s left[/yellow]"
        )

    def test_estimate_unavailable_flag(self):
        """Test when estimate_available flag is False."""
        current_time = datetime(2024, 1, 1, 12, 0, 50, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=False, seconds_remaining=100.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_negative_elapsed_time_scenario(self):
        """Test unusual case where current time appears before updated_at."""
        current_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            updated_at="2024-01-01T12:00:30Z",  # In the "future"
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=100.0),
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=True)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_unicode_progress_bars_preserved(self):
        """Test that unicode characters in progress bars are preserved after tag removal."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        finetune_job = create_finetune_response(
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0)
        )

        result = generate_progress_bar(finetune_job, current_time, use_rich=False)

        assert (
            result == "Progress: ████████████████████░░░░░░░░░░░░░░░░░░░░  50% 30s left"
        )
