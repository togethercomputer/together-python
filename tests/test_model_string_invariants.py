import pytest

def normalize_model_name(name: str) -> str:
    if not name or not isinstance(name, str):
        return ""
    return name.strip()

def test_model_name_trimming():
    assert normalize_model_name("  meta-llama/Llama-3-70b-chat-hf  ") == "meta-llama/Llama-3-70b-chat-hf"
    assert normalize_model_name("mistralai/Mixtral-8x7B-Instruct-v0.1") == "mistralai/Mixtral-8x7B-Instruct-v0.1"

def test_empty_model_name():
    assert normalize_model_name("") == ""
    assert normalize_model_name("   ") == ""
