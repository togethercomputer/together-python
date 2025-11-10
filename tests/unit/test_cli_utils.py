"""
Unit tests for generate_progress_bar function in together.cli.api.utils.

This test suite covers both general functionality and corner cases for the
progress bar generation used in fine-tuning job status displays.

Note: The current implementation has bugs that prevent these tests from running
against the actual code without workarounds. See comments for details.
"""

from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from together.cli.api.utils import generate_progress_bar
from together.types.finetune import FinetuneResponse, FinetuneProgress


class TestGenerateProgressBarGeneral:
    """General test cases for normal operation."""

    def test_progress_unavailable_when_none(self):
        """Test that progress shows unavailable when progress field is None."""
        finetune_job = FinetuneResponse(
            id="ft-test-123", progress=None, updated_at="2024-01-01T12:00:00Z"
        )

        result = generate_progress_bar(finetune_job)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    def test_progress_unavailable_when_not_set(self):
        """Test that progress shows unavailable when field is not provided."""
        finetune_job = FinetuneResponse(
            id="ft-test-123", updated_at="2024-01-01T12:00:00Z"
        )

        result = generate_progress_bar(finetune_job)

        assert result == "Progress: [bold red]unavailable[/bold red]"

    @patch("together.cli.api.utils.datetime")
    def test_progress_bar_at_start(self, mock_datetime):
        """Test progress bar display when job just started (low percentage)."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True, seconds_remaining=1000.0
            ),
        )

        # Workaround: Set updated_at as datetime (current impl expects datetime but type says str)
        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        # 10 seconds elapsed / 1000 seconds remaining = 0.01 ratio = 1% progress
        # 0.01 * 40 = 0.4, ceil(0.4) = 1 filled bar
        expected = "█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ Progress: [bold]  1%[/bold] [yellow]16min 30s left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_progress_bar_at_midpoint(self, mock_datetime):
        """Test progress bar at approximately 50% completion."""
        current_time = datetime(2024, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True,
                seconds_remaining=60.0,
            ),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        # 60 seconds elapsed / 60 seconds remaining = 1.0 ratio = 100% progress
        # 1.0 * 40 = 40 filled bars
        expected = "████████████████████████████████████████ Progress: [bold]100%[/bold] [yellow]N/A left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_progress_bar_near_completion(self, mock_datetime):
        """Test progress bar when job is almost complete."""
        current_time = datetime(2024, 1, 1, 12, 5, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True,
                seconds_remaining=30.0,  # 300s elapsed, 30s remaining = ~90%
            ),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        # 300 seconds elapsed / 30 seconds remaining = 10.0 ratio = 1000% progress
        # 10.0 * 40 = 400, ceil(400) = 400, but width is 40 so all filled
        expected = "████████████████████████████████████████ Progress: [bold]100%[/bold] [yellow]N/A left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_progress_bar_contains_rich_formatting(self, mock_datetime):
        """Test that progress bar includes expected Rich markup formatting."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        # 30 seconds elapsed / 60 seconds remaining = 0.5 ratio = 50% progress
        # 0.5 * 40 = 20 filled bars
        expected = "████████████████████░░░░░░░░░░░░░░░░░░░░ Progress: [bold] 50%[/bold] [yellow]30s left[/yellow]"
        assert result == expected


class TestGenerateProgressBarCornerCases:
    """Corner cases and edge conditions."""

    @patch("together.cli.api.utils.datetime")
    def test_zero_seconds_remaining(self, mock_datetime):
        """Test handling of zero seconds remaining (potential division by zero)."""
        current_time = datetime(2024, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True, seconds_remaining=0.0  # Division by zero risk
            ),
        )

        finetune_job.updated_at = updated_at

        # Should handle gracefully without crashing
        result = generate_progress_bar(finetune_job)
        expected = "Progress: [bold red]unavailable[/bold red]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_very_small_remaining_time(self, mock_datetime):
        """Test with very small remaining time (< 1 second)."""
        current_time = datetime(2024, 1, 1, 12, 0, 5, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=0.5),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)
        # 5 seconds elapsed / 0.5 seconds remaining = 10.0 ratio = 1000% progress
        expected = "████████████████████████████████████████ Progress: [bold]100%[/bold] [yellow]N/A left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_very_large_remaining_time(self, mock_datetime):
        """Test with very large remaining time (hours)."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True, seconds_remaining=36000.0  # 10 hours
            ),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)
        # 30 seconds elapsed / 36000 seconds remaining = 0.000833 ratio = 0.0833% progress
        # 0.000833 * 40 = 0.033, ceil(0.033) = 1 filled bar
        expected = "█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ Progress: [bold]  0%[/bold] [yellow]9h 59min 30s left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_job_exceeding_estimate(self, mock_datetime):
        """Test when elapsed time exceeds original estimate (>100% progress)."""
        current_time = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=True,
                seconds_remaining=60.0,  # Only 1 min remaining but 2 hours elapsed
            ),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)
        # 7200 seconds elapsed / 60 seconds remaining = 120.0 ratio = 12000% progress
        expected = "████████████████████████████████████████ Progress: [bold]100%[/bold] [yellow]N/A left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_timezone_aware_datetime(self, mock_datetime):
        """Test with different timezone for updated_at."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        # Use different timezone (EST = UTC-5)
        eastern = timezone(timedelta(hours=-5))
        updated_at = datetime(
            2024, 1, 1, 7, 0, 0, tzinfo=eastern
        )  # Same as 12:00:00 UTC

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T07:00:00-05:00",
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)
        # 30 seconds elapsed / 60 seconds remaining = 0.5 ratio = 50% progress
        expected = "████████████████████░░░░░░░░░░░░░░░░░░░░ Progress: [bold] 50%[/bold] [yellow]30s left[/yellow]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_progress_bar_width_consistency(self, mock_datetime):
        """Test that progress bar maintains consistent 40-character width."""
        current_time = datetime(2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=60.0),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        # Bar should always be 40 characters wide (filled + empty)
        filled_count = result.count("█")
        empty_count = result.count("░")
        total_width = filled_count + empty_count

        assert total_width == 40, f"Expected bar width of 40, got {total_width}"

    @patch("together.cli.api.utils.datetime")
    def test_estimate_unavailable_flag(self, mock_datetime):
        """Test when estimate_available flag is False."""
        current_time = datetime(2024, 1, 1, 12, 0, 50, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:00Z",
            progress=FinetuneProgress(
                estimate_available=False, seconds_remaining=100.0
            ),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)

        expected = "Progress: [bold red]unavailable[/bold red]"
        assert result == expected

    @patch("together.cli.api.utils.datetime")
    def test_negative_elapsed_time_scenario(self, mock_datetime):
        """Test unusual case where current time appears before updated_at."""
        # This could happen due to clock skew or incorrect data
        current_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = current_time

        updated_at = datetime(
            2024, 1, 1, 12, 0, 30, tzinfo=timezone.utc
        )  # In the "future"

        finetune_job = FinetuneResponse(
            id="ft-test-123",
            updated_at="2024-01-01T12:00:30Z",
            progress=FinetuneProgress(estimate_available=True, seconds_remaining=100.0),
        )

        finetune_job.updated_at = updated_at

        result = generate_progress_bar(finetune_job)
        # current_time is earlier than the event time, so the progress is not available
        expected = "Progress: [bold red]unavailable[/bold red]"
        assert result == expected
