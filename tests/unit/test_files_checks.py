import json
import pytest
from pathlib import Path

from together.constants import MIN_SAMPLES
from together.utils.files import check_file

_TEST_PREFERENCE_OPENAI_CONTENT = [
    {
        "input": {
            "messages": [
                {"role": "user", "content": "Hi there, I have a question."},
                {"role": "assistant", "content": "Hello, how is your day going?"},
                {
                    "role": "user",
                    "content": "Hello, can you tell me how cold San Francisco is today?",
                },
            ],
        },
        "preferred_output": [
            {
                "role": "assistant",
                "content": "Today in San Francisco, it is not quite cold as expected. Morning clouds will give away "
                "to sunshine, with a high near 68°F (20°C) and a low around 57°F (14°C).",
            }
        ],
        "non_preferred_output": [
            {
                "role": "assistant",
                "content": "It is not particularly cold in San Francisco today.",
            }
        ],
    },
    {
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": "What's the best way to learn programming?",
                },
            ],
        },
        "preferred_output": [
            {
                "role": "assistant",
                "content": "The best way to learn programming is through consistent practice, working on real projects, "
                "and breaking down complex problems into smaller parts. Start with a beginner-friendly language like Python.",
            }
        ],
        "non_preferred_output": [
            {"role": "assistant", "content": "Just read some books and you'll be fine."}
        ],
    },
]


def test_check_jsonl_valid_general(tmp_path: Path):
    # Create a valid JSONL file
    file = tmp_path / "valid.jsonl"
    content = [{"text": "Hello, world!"}, {"text": "How are you?"}]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


def test_check_jsonl_valid_instruction(tmp_path: Path):
    # Create a valid JSONL file with instruction format
    file = tmp_path / "valid_instruction.jsonl"
    content = [
        {"prompt": "Translate the following sentence.", "completion": "Hello, world!"},
        {
            "prompt": "Summarize the text.",
            "completion": "Weyland-Yutani Corporation creates advanced AI.",
        },
    ]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


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
        {
            "messages": [
                {"role": "system", "content": "You are a kind AI"},
                {"role": "user", "content": "How are you?"},
                {"role": "assistant", "content": "I am fine."},
            ]
        },
    ]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


def test_check_jsonl_valid_conversational_multiple_turns(tmp_path: Path):
    # Create a valid JSONL file with conversational format and multiple user-assistant turn pairs
    file = tmp_path / "valid_conversational_multiple_turns.jsonl"
    content = _TEST_PREFERENCE_OPENAI_CONTENT
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


def test_check_jsonl_valid_preference_openai(tmp_path: Path):
    file = tmp_path / "valid_preference_openai.jsonl"
    content = _TEST_PREFERENCE_OPENAI_CONTENT
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


def test_check_jsonl_invalid_preference_openai_missing_fields(tmp_path: Path):
    # Test all required fields in OpenAI preference format
    required_fields = [
        ("input", "Missing input field"),
        ("preferred_output", "Missing preferred_output field"),
        ("non_preferred_output", "Missing non_preferred_output field"),
    ]

    for field_to_remove, description in required_fields:
        file = tmp_path / f"invalid_preference_openai_missing_{field_to_remove}.jsonl"
        content = [item.copy() for item in _TEST_PREFERENCE_OPENAI_CONTENT]

        # Remove the specified field from the first item
        del content[0][field_to_remove]

        with file.open("w") as f:
            f.write("\n".join(json.dumps(item) for item in content))

        report = check_file(file)

        assert not report["is_check_passed"], f"Test should fail when {description}"


def test_check_jsonl_invalid_preference_openai_structural_issues(tmp_path: Path):
    # Test various structural issues in OpenAI preference format
    test_cases = [
        {
            "name": "empty_messages",
            "modifier": lambda item: item.update({"input": {"messages": []}}),
            "description": "Empty messages array",
        },
        {
            "name": "missing_role_preferred",
            "modifier": lambda item: item.update(
                {"preferred_output": [{"content": "Missing role field"}]}
            ),
            "description": "Missing role in preferred_output",
        },
        {
            "name": "missing_role_non_preferred",
            "modifier": lambda item: item.update(
                {"non_preferred_output": [{"content": "Missing role field"}]}
            ),
            "description": "Missing role in non_preferred_output",
        },
        {
            "name": "wrong_output_format_preferred",
            "modifier": lambda item: item.update(
                {"preferred_output": "Not an array but a string"}
            ),
            "description": "Wrong format for preferred_output",
        },
        {
            "name": "wrong_output_format_non_preferred",
            "modifier": lambda item: item.update(
                {"non_preferred_output": "Not an array but a string"}
            ),
            "description": "Wrong format for non_preferred_output",
        },
        {
            "name": "missing_content",
            "modifier": lambda item: item.update(
                {"input": {"messages": [{"role": "user"}]}}
            ),
            "description": "Missing content in messages",
        },
        {
            "name": "multiple_preferred_outputs",
            "modifier": lambda item: item.update(
                {
                    "preferred_output": [
                        {"role": "assistant", "content": "First response"},
                        {"role": "assistant", "content": "Second response"},
                    ]
                }
            ),
            "description": "Multiple messages in preferred_output",
        },
        {
            "name": "multiple_non_preferred_outputs",
            "modifier": lambda item: item.update(
                {
                    "non_preferred_output": [
                        {"role": "assistant", "content": "First response"},
                        {"role": "assistant", "content": "Second response"},
                    ]
                }
            ),
            "description": "Multiple messages in non_preferred_output",
        },
        {
            "name": "empty_preferred_output",
            "modifier": lambda item: item.update({"preferred_output": []}),
            "description": "Empty preferred_output array",
        },
        {
            "name": "empty_non_preferred_output",
            "modifier": lambda item: item.update({"non_preferred_output": []}),
            "description": "Empty non_preferred_output array",
        },
    ]

    for test_case in test_cases:
        file = tmp_path / f"invalid_preference_openai_{test_case['name']}.jsonl"
        content = [item.copy() for item in _TEST_PREFERENCE_OPENAI_CONTENT]

        # Apply the modification to the first item
        test_case["modifier"](content[0])

        with file.open("w") as f:
            f.write("\n".join(json.dumps(item) for item in content))

        report = check_file(file)

        assert not report[
            "is_check_passed"
        ], f"Test should fail with {test_case['description']}"


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
        f.write("\n".join(json.dumps(item) for item in content))

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
        f.write("\n".join(json.dumps(item) for item in content))

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
        f.write("\n".join(json.dumps(item) for item in content))

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
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert "Found invalid role `invalid_role`" in report["message"]


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
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert not report["is_check_passed"]
    assert "Invalid role turns" in report["message"]


def test_check_jsonl_invalid_value_type(tmp_path: Path):
    # Create a JSONL file with an invalid value type
    file = tmp_path / "invalid_value_type.jsonl"
    content = [{"text": 123}]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

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
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert "Field `content` is missing for a turn" in report["message"]


def test_check_jsonl_wrong_turn_type(tmp_path: Path):
    file = tmp_path / "wrong_turn_type.jsonl"
    content = [
        {
            "messages": [
                "Hi!",
                {"role": "user", "content": "Hi"},
                {"role": "assistant"},
            ]
        }
    ]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert (
        "Invalid format on line 1 of the input file. Expected a dictionary"
        in report["message"]
    )


def test_check_jsonl_extra_column(tmp_path: Path):
    file = tmp_path / "extra_column.jsonl"
    content = [{"text": "Hello, world!", "extra_column": "extra"}]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert "Found extra column" in report["message"]


def test_check_jsonl_empty_messages(tmp_path: Path):
    file = tmp_path / "empty_messages.jsonl"
    content = [{"messages": []}]
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)
    assert not report["is_check_passed"]
    assert (
        "Expected a non-empty list of messages. Found empty list" in report["message"]
    )
