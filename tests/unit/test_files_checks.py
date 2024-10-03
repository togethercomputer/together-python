import pytest
from pathlib import Path
from together.utils.files import check_file


def test_check_jsonl_valid_general(tmp_path: Path):
    # Create a valid JSONL file
    file = tmp_path / "valid.jsonl"
    content = [
        '{"text": "Hello, world!"}',
        '{"text": "How are you?"}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == 2
    assert report["min_samples"]


def test_check_jsonl_valid_instruction(tmp_path: Path):
    # Create a valid JSONL file with instruction format
    file = tmp_path / "valid_instruction.jsonl"
    content = [
        '{"prompt": "Translate the following sentence.", "completion": "Hello, world!"}',
        '{"prompt": "Summarize the text.", "completion": "OpenAI creates advanced AI."}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == 2
    assert report["min_samples"]


def test_check_jsonl_valid_conversational_single_turn(tmp_path: Path):
    # Create a valid JSONL file with conversational format and 1 user-assistant turn pair
    file = tmp_path / "valid_conversational_single_turn.jsonl"
    content = [
        '{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}',
        '{"messages": [{"role": "user", "content": "How are you?"}, {"role": "assistant", "content": "I am fine."}]}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    print(report)
    
    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == 2
    assert report["min_samples"]


def test_check_jsonl_valid_conversational_multiple_turns(tmp_path: Path):
    # Create a valid JSONL file with conversational format and multiple user-assistant turn pairs
    file = tmp_path / "valid_conversational_multiple_turns.jsonl"
    content = [
        '{"messages": [{"role": "user", "content": "Is it going to rain today?"}, {"role": "assistant", "content": "Yes, expect showers in the afternoon."}]}',
        '{"messages": [{"role": "user", "content": "Who won the game last night?"}, {"role": "assistant", "content": "The home team won by two points."}]}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == 2
    assert report["min_samples"]


def test_check_jsonl_empty_file(tmp_path: Path):
    # Create an empty JSONL file
    file = tmp_path / "empty.jsonl"
    file.touch()
    
    report = check_file(file)
    
    print(report)
    
    assert not report["is_check_passed"]
    assert report["message"] == "File is empty"
    assert report["file_size"] == 0


def test_check_jsonl_non_utf8(tmp_path: Path):
    # Create a non-UTF-8 encoded JSONL file
    file = tmp_path / "non_utf8.jsonl"
    file.write_bytes(b'\xff\xfe\xfd')
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert not report["utf8"]
    assert "File is not UTF-8 encoded." in report["message"]


def test_check_jsonl_invalid_json(tmp_path: Path):
    # Create a JSONL file with invalid JSON
    file = tmp_path / "invalid_json.jsonl"
    content = [
        '{"text": "Hello, world!"}',
        'Invalid JSON Line'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert "Error parsing json payload" in report["message"]


def test_check_jsonl_missing_required_field(tmp_path: Path):
    # Create a JSONL file missing a required field
    file = tmp_path / "missing_field.jsonl"
    content = [
        '{"prompt": "Translate the following sentence.", "completion": "Hello, world!"}',
        '{"prompt": "Summarize the text."}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert "Missing 'completion' field was found on line 2" in report["message"]


def test_check_jsonl_inconsistent_dataset_format(tmp_path: Path):
    # Create a JSONL file with inconsistent dataset formats
    file = tmp_path / "inconsistent_format.jsonl"
    content = [
        '{"messages": [{"role": "user", "content": "Hi"}]}',
        '{"text": "How are you?"}'  # Missing 'messages'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert "All samples in the dataset must have the same dataset format" in report["message"]


def test_check_jsonl_invalid_role(tmp_path: Path):
    # Create a JSONL file with an invalid role
    file = tmp_path / "invalid_role.jsonl"
    content = [
        '{"messages": [{"role": "invalid_role", "content": "Hi"}]}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert "Found invalid role 'invalid_role'" in report["message"]


def test_check_jsonl_non_alternating_roles(tmp_path: Path):
    # Create a JSONL file with non-alternating user/assistant roles
    file = tmp_path / "non_alternating_roles.jsonl"
    content = [
        '{"messages": [{"role": "user", "content": "Hi"}, {"role": "user", "content": "Hello again"}]}'
    ]
    file.write_text("\n".join(content), encoding="utf-8")
    
    report = check_file(file)
    
    assert not report["is_check_passed"]
    assert "Invalid role turns" in report["message"]
