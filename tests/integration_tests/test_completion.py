import os

import pytest

from together.client import Together
from together.types import CompletionResponse
from together.types.common import ObjectType, UsageData
from together.types.completions import CompletionChoicesData

from generate_hyperparameters import (
    random_max_tokens,
    random_repetition_penalty,
    random_temperature,
    random_top_k,
    random_top_p,
)


class TestTogetherCompletion:
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
        random_max_tokens,
        random_temperature,
        random_top_p,
        random_top_k,
        random_repetition_penalty,
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
