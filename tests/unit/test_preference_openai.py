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


def test_check_jsonl_valid_preference_openai(tmp_path: Path):
    """Test valid preference OpenAI format."""
    file = tmp_path / "valid_preference_openai.jsonl"
    content = _TEST_PREFERENCE_OPENAI_CONTENT
    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert report["is_check_passed"]
    assert report["utf8"]
    assert report["num_samples"] == len(content)
    assert report["has_min_samples"]


MISSING_FIELDS_TEST_CASES = [
    pytest.param("input", "Missing input field", id="missing_input"),
    pytest.param(
        "preferred_output",
        "Missing preferred_output field",
        id="missing_preferred_output",
    ),
    pytest.param(
        "non_preferred_output",
        "Missing non_preferred_output field",
        id="missing_non_preferred_output",
    ),
]


@pytest.mark.parametrize("field_to_remove, description", MISSING_FIELDS_TEST_CASES)
def test_check_jsonl_invalid_preference_openai_missing_fields(
    tmp_path: Path, field_to_remove, description
):
    """Test missing required fields in OpenAI preference format."""
    file = tmp_path / f"invalid_preference_openai_missing_{field_to_remove}.jsonl"
    content = [item.copy() for item in _TEST_PREFERENCE_OPENAI_CONTENT]

    # Remove the specified field from the first item
    del content[0][field_to_remove]

    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert not report["is_check_passed"], f"Test should fail when {description}"


STRUCTURAL_ISSUE_TEST_CASES = [
    pytest.param(
        "empty_messages",
        lambda item: item.update({"input": {"messages": []}}),
        "Empty messages array",
        id="empty_messages",
    ),
    pytest.param(
        "missing_role_preferred",
        lambda item: item.update(
            {"preferred_output": [{"content": "Missing role field"}]}
        ),
        "Missing role in preferred_output",
        id="missing_role_preferred",
    ),
    pytest.param(
        "missing_role_non_preferred",
        lambda item: item.update(
            {"non_preferred_output": [{"content": "Missing role field"}]}
        ),
        "Missing role in non_preferred_output",
        id="missing_role_non_preferred",
    ),
    pytest.param(
        "missing_content_preferred",
        lambda item: item.update({"preferred_output": [{"role": "assistant"}]}),
        "Missing content in preferred_output",
        id="missing_content_preferred",
    ),
    pytest.param(
        "missing_content_non_preferred",
        lambda item: item.update({"non_preferred_output": [{"role": "assistant"}]}),
        "Missing content in non_preferred_output",
        id="missing_content_non_preferred",
    ),
    pytest.param(
        "wrong_output_format_preferred",
        lambda item: item.update({"preferred_output": "Not an array but a string"}),
        "Wrong format for preferred_output",
        id="wrong_output_format_preferred",
    ),
    pytest.param(
        "wrong_output_format_non_preferred",
        lambda item: item.update({"non_preferred_output": "Not an array but a string"}),
        "Wrong format for non_preferred_output",
        id="wrong_output_format_non_preferred",
    ),
    pytest.param(
        "missing_content",
        lambda item: item.update({"input": {"messages": [{"role": "user"}]}}),
        "Missing content in messages",
        id="missing_content",
    ),
    pytest.param(
        "multiple_preferred_outputs",
        lambda item: item.update(
            {
                "preferred_output": [
                    {"role": "assistant", "content": "First response"},
                    {"role": "assistant", "content": "Second response"},
                ]
            }
        ),
        "Multiple messages in preferred_output",
        id="multiple_preferred_outputs",
    ),
    pytest.param(
        "multiple_non_preferred_outputs",
        lambda item: item.update(
            {
                "non_preferred_output": [
                    {"role": "assistant", "content": "First response"},
                    {"role": "assistant", "content": "Second response"},
                ]
            }
        ),
        "Multiple messages in non_preferred_output",
        id="multiple_non_preferred_outputs",
    ),
    pytest.param(
        "empty_preferred_output",
        lambda item: item.update({"preferred_output": []}),
        "Empty preferred_output array",
        id="empty_preferred_output",
    ),
    pytest.param(
        "empty_non_preferred_output",
        lambda item: item.update({"non_preferred_output": []}),
        "Empty non_preferred_output array",
        id="empty_non_preferred_output",
    ),
    pytest.param(
        "non_string_content_in_messages",
        lambda item: item.update(
            {"input": {"messages": [{"role": "user", "content": 123}]}}
        ),
        "Non-string content in messages",
        id="non_string_content_in_messages",
    ),
    pytest.param(
        "invalid_role_in_messages",
        lambda item: item.update(
            {"input": {"messages": [{"role": "invalid_role", "content": "Hello"}]}}
        ),
        "Invalid role in messages",
        id="invalid_role_in_messages",
    ),
    pytest.param(
        "non_alternating_roles",
        lambda item: item.update(
            {
                "input": {
                    "messages": [
                        {"role": "user", "content": "Hello"},
                        {"role": "user", "content": "How are you?"},
                    ]
                }
            }
        ),
        "Non-alternating roles in messages",
        id="non_alternating_roles",
    ),
    pytest.param(
        "invalid_weight_type",
        lambda item: item.update(
            {
                "input": {
                    "messages": [
                        {"role": "user", "content": "Hello", "weight": "not_an_integer"}
                    ]
                }
            }
        ),
        "Invalid weight type",
        id="invalid_weight_type",
    ),
    pytest.param(
        "invalid_weight_value",
        lambda item: item.update(
            {"input": {"messages": [{"role": "user", "content": "Hello", "weight": 2}]}}
        ),
        "Invalid weight value",
        id="invalid_weight_value",
    ),
    pytest.param(
        "non_dict_message",
        lambda item: item.update({"input": {"messages": ["Not a dictionary"]}}),
        "Non-dictionary message",
        id="non_dict_message",
    ),
    pytest.param(
        "non_dict_input",
        lambda item: item.update({"input": "Not a dictionary"}),
        "Non-dictionary input",
        id="non_dict_input",
    ),
    pytest.param(
        "missing_messages_in_input",
        lambda item: item.update({"input": {}}),
        "Missing messages in input",
        id="missing_messages_in_input",
    ),
    pytest.param(
        "non_assistant_role_in_preferred",
        lambda item: item.update(
            {
                "preferred_output": [
                    {"role": "user", "content": "This should be assistant"}
                ]
            }
        ),
        "Non-assistant role in preferred output",
        id="non_assistant_role_in_preferred",
    ),
    pytest.param(
        "non_assistant_role_in_non_preferred",
        lambda item: item.update(
            {
                "non_preferred_output": [
                    {"role": "user", "content": "This should be assistant"}
                ]
            }
        ),
        "Non-assistant role in non-preferred output",
        id="non_assistant_role_in_non_preferred",
    ),
]


@pytest.mark.parametrize("name, modifier, description", STRUCTURAL_ISSUE_TEST_CASES)
def test_check_jsonl_invalid_preference_openai_structural_issues(
    tmp_path: Path, name, modifier, description
):
    """Test various structural issues in OpenAI preference format."""
    file = tmp_path / f"invalid_preference_openai_{name}.jsonl"
    content = [item.copy() for item in _TEST_PREFERENCE_OPENAI_CONTENT]

    # Apply the modification to the first item
    modifier(content[0])

    with file.open("w") as f:
        f.write("\n".join(json.dumps(item) for item in content))

    report = check_file(file)

    assert not report["is_check_passed"], f"Test should fail with {description}"
