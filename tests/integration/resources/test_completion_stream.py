import os

import pytest

from together.client import Together
from together.types import CompletionResponse
from together.types.common import ObjectType, UsageData
from together.types.completions import CompletionChoicesData

from .generate_hyperparameters import (
    random_max_tokens,  # noqa
    random_repetition_penalty,  # noqa
    random_temperature,  # noqa
    random_top_k,  # noqa
    random_top_p,  # noqa
)


class TestTogetherCompletionStream:
    @pytest.fixture
    def sync_together_client(self) -> Together:
        """
        Initialize object with mocked API key
        """
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        return Together(api_key=TOGETHER_API_KEY)

    def test_create(
        self,
        sync_together_client,
        random_max_tokens,  # noqa
        random_temperature,  # noqa
        random_top_p,  # noqa
        random_top_k,  # noqa
        random_repetition_penalty,  # noqa
    ) -> None:
        prompt = "The space robots have"
        model = "mistralai/Mixtral-8x7B-v0.1"
        stop = ["</s>"]

        # max_tokens should be a reasonable number for this test
        assert 0 < random_max_tokens < 1024

        assert 0 <= random_temperature <= 2

        assert 0 <= random_top_p <= 1

        assert 1 <= random_top_k <= 100

        assert 0 <= random_repetition_penalty <= 2

        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=stop,
            max_tokens=random_max_tokens,
            temperature=random_temperature,
            top_p=random_top_p,
            top_k=random_top_k,
            repetition_penalty=random_repetition_penalty,
            echo=True,
        )

        assert isinstance(response, CompletionResponse)

        assert isinstance(response.id, str)
        assert isinstance(response.created, int)
        assert isinstance(response.object, ObjectType)
        assert response.model == model
        assert isinstance(response.choices, list)
        assert isinstance(response.choices[0], CompletionChoicesData)
        assert isinstance(response.choices[0].text, str)
        assert isinstance(response.prompt, list)
        assert isinstance(response.prompt[0].text, str)
        assert isinstance(response.usage, UsageData)
        assert isinstance(response.usage.prompt_tokens, int)
        assert isinstance(response.usage.completion_tokens, int)
        assert isinstance(response.usage.total_tokens, int)
        assert (
            response.usage.prompt_tokens + response.usage.completion_tokens
            == response.usage.total_tokens
        )

    def test_prompt(self):
        pass

    def test_no_prompt(self):
        pass

    def test_model(self):
        pass

    def test_no_model(self):
        pass

    def test_max_tokens(self):
        pass

    def test_no_max_tokens(self):
        pass

    def test_high_max_tokens(self):
        pass

    def test_stop(self):
        pass

    def test_no_stop(self):
        pass

    def test_temperature(self):
        pass

    def test_top_p(self):
        pass

    def test_top_k(self):
        pass

    def test_repetition_penalty(self):
        pass

    def test_echo(self):
        pass

    def test_n(self):
        pass

    def test_safety_model(self):
        pass
