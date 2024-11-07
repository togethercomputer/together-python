import json
import pytest
from pathlib import Path

from together.constants import MIN_SAMPLES
from together.utils.files import check_file


def test_check_jsonl_valid_general(tmp_path: Path):
    # Create a valid JSONL file
    file = tmp_path / "valid.jsonl"
    content = [{"text": "Hello, world!"}, {"text": "How are you?"}]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["min_samples"] >= MIN_SAMPLES


def test_check_jsonl_valid_instruction(tmp_path: Path):
    # Create a valid JSONL file with instruction format
    file = tmp_path / "valid_instruction.jsonl"
    content = [
        {"prompt": "Translate the following sentence.", "completion": "Hello, world!"},
        {"prompt": "Summarize the text.", "completion": "OpenAI creates advanced AI."},
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["min_samples"] >= MIN_SAMPLES


def test_check_jsonl_valid_conversational_single_turn(tmp_path: Path):
    # Create a valid JSONL file with conversational format and 1 user-assistant turn pair
    file = tmp_path / "valid_conversational_single_turn.jsonl"
    content = [
        {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "How are you?"},
                {"role": "assistant", "content": "I am fine."},
            ]
        },
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["min_samples"] >= MIN_SAMPLES


def test_check_jsonl_valid_conversational_multiple_turns(tmp_path: Path):
    # Create a valid JSONL file with conversational format and multiple user-assistant turn pairs
    file = tmp_path / "valid_conversational_multiple_turns.jsonl"
    content = [
        {
            "messages": [
                {"role": "user", "content": "Is it going to rain today?"},
                {
                    "role": "assistant",
                    "content": "Yes, expect showers in the afternoon.",
                },
                {"role": "user", "content": "What is the weather like in Tokyo?"},
                {"role": "assistant", "content": "It is sunny with a chance of rain."},
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Who won the game last night?"},
                {"role": "assistant", "content": "The home team won by two points."},
                {"role": "user", "content": "What is the weather like in Amsterdam?"},
                {"role": "assistant", "content": "It is cloudy with a chance of snow."},
            ]
        },
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["min_samples"] >= MIN_SAMPLES


def test_check_jsonl_empty_file(tmp_path: Path):
    # Create an empty JSONL file
    file = tmp_path / "empty.jsonl"
    file.touch()

    report = check_file(file)

    assert not report["is_check_passed"]
    assert report["message"] == "File is empty"
    assert report["file_size"] == 0


def test_check_jsonl_non_utf8(tmp_path: Path):
    # Create a non-UTF-8 encoded JSONL file
    file = tmp_path / "non_utf8.jsonl"
    file.write_bytes(b"\xff\xfe\xfd")

    report = check_file(file)

    assert not report["is_check_passed"]
    assert not report["utf8"]
    assert "File is not UTF-8 encoded." in report["message"]


def test_check_jsonl_invalid_json(tmp_path: Path):
    # Create a JSONL file with invalid JSON
    file = tmp_path / "invalid_json.jsonl"
    content = [{"text": "Hello, world!"}, "Invalid JSON Line"]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert "Error parsing file." in report["message"]


def test_check_jsonl_missing_required_field(tmp_path: Path):
    # Create a JSONL file missing a required field
    file = tmp_path / "missing_field.jsonl"
    content = [
        {"prompt": "Translate the following sentence.", "completion": "Hello, world!"},
        {"prompt": "Summarize the text."},
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert (
        "Error parsing file. Could not detect a format for the line 2"
        in report["message"]
    )


def test_check_jsonl_inconsistent_dataset_format(tmp_path: Path):
    # Create a JSONL file with inconsistent dataset formats
    file = tmp_path / "inconsistent_format.jsonl"
    content = [
        {"messages": [{"role": "user", "content": "Hi"}]},
        {"text": "How are you?"},  # Missing 'messages'
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert (
        "All samples in the dataset must have the same dataset format"
        in report["message"]
    )


def test_check_jsonl_invalid_role(tmp_path: Path):
    # Create a JSONL file with an invalid role
    file = tmp_path / "invalid_role.jsonl"
    content = [{"messages": [{"role": "invalid_role", "content": "Hi"}]}]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert "Found invalid role 'invalid_role'" in report["message"]


def test_check_jsonl_non_alternating_roles(tmp_path: Path):
    # Create a JSONL file with non-alternating user/assistant roles
    file = tmp_path / "non_alternating_roles.jsonl"
    content = [
        {
            "messages": [
                {"role": "user", "content": "Hi"},
                {"role": "user", "content": "Hello again"},
            ]
        }
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert "Invalid role turns" in report["message"]


def test_check_jsonl_invalid_value_type(tmp_path: Path):
    # Create a JSONL file with an invalid value type
    file = tmp_path / "invalid_value_type.jsonl"
    content = [{"text": 123}]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert "Expected string" in report["message"]


def test_check_jsonl_missing_field_in_conversation(tmp_path: Path):
    file = tmp_path / "missing_field_in_conversation.jsonl"
    content = [
        {
            "messages": [
                {"role": "user", "content": "Hi"},
                {"role": "assistant"},
            ]
        }
    ]
    with file.open("w") as f:
        f.write("\n".join([json.dumps(item) for item in content]))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert "Field 'content' is missing for a turn" in report["message"]
