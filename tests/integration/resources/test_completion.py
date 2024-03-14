import os

import pytest

from itertools import product

from together.client import Together
from together.types import CompletionResponse
from together.types.common import ObjectType, UsageData
from together.types.completions import CompletionChoicesData
from together.error import InvalidRequestError

from ..constants import completion_test_model_list, moderation_test_model_list
from .generate_hyperparameters import (
    random_max_tokens,  # noqa
    random_repetition_penalty,  # noqa
    random_temperature,  # noqa
    random_top_k,  # noqa
    random_top_p,  # noqa
)

STOP = ["</s>"]


class TestTogetherCompletion:
    @pytest.fixture
    def sync_together_client(self) -> Together:
        """
        Initialize object with mocked API key
        """
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        return Together(api_key=TOGETHER_API_KEY)

    @pytest.mark.parametrize("model", completion_test_model_list)
    def test_create(
        self,
        model,
        sync_together_client,
        random_max_tokens,  # noqa
        random_temperature,  # noqa
        random_top_p,  # noqa
        random_top_k,  # noqa
        random_repetition_penalty,  # noqa
    ) -> None:
        """
        Tests structure and typing
        """
        prompt = "The space robots have"

        # max_tokens should be a reasonable number for this test
        assert 0 < random_max_tokens < 1024

        assert 0 <= random_temperature <= 2

        assert 0 <= random_top_p <= 1

        assert 1 <= random_top_k <= 100

        assert 0 <= random_repetition_penalty <= 2

        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
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

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_prompt(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            echo=True,
        )

        assert isinstance(response, CompletionResponse)

        assert response.prompt[0].text == prompt

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_no_prompt(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(TypeError):
            response = sync_together_client.completions.create(
                model=model,
                stop=STOP,
                max_tokens=10,
                echo=True,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_model(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            echo=True,
        )

        assert isinstance(response, CompletionResponse)

        assert response.model == model

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_no_model(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(TypeError):
            response = sync_together_client.completions.create(
                prompt=prompt,
                stop=STOP,
                max_tokens=10,
                echo=True,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_max_tokens(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=1,
        )

        assert isinstance(response, CompletionResponse)

        assert response.usage.completion_tokens == 1

    @pytest.mark.parametrize(
        "model,prompt,max_tokens",
        product(
            completion_test_model_list,
            ["This is a test", "hi," * 25],
            [35000, 40000, 50000],
        ),
    )
    def test_high_max_tokens(
        self,
        model,
        prompt,
        max_tokens,
        sync_together_client,
    ):
        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=max_tokens,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, ["This is a test", "hi," * 25]),
    )
    def test_echo(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt, model=model, stop=STOP, max_tokens=1, echo=True, logprobs=1
        )

        assert isinstance(response, CompletionResponse)

        assert response.prompt[0].text == prompt
        assert isinstance(response.prompt[0].logprobs.tokens, list)
        assert isinstance(response.prompt[0].logprobs.token_logprobs, list)

    @pytest.mark.parametrize(
        "model,prompt,n",
        product(
            completion_test_model_list, ["This is a test", "hi," * 25], [1, 2, 3, 4]
        ),
    )
    def test_n(
        self,
        model,
        prompt,
        n,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt, model=model, stop=STOP, max_tokens=1, n=n, temperature=0.5
        )

        assert isinstance(response, CompletionResponse)

        assert len(response.choices) == n

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            ["This is a test", "hi," * 25],
        ),
    )
    def test_high_n(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        MAX_N = 128
        n = MAX_N + 1

        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=1,
                n=n,
                temperature=0.1,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            ["This is a test", "hi," * 25],
        ),
    )
    def test_n_with_no_sample(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        MAX_N = 128
        n = MAX_N + 1

        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=1,
                n=n,
            )

    @pytest.mark.parametrize(
        "model,prompt,safety_model",
        product(
            completion_test_model_list,
            ["This is a test", "hi," * 25],
            moderation_test_model_list,
        ),
    )
    def test_safety_model(
        self,
        model,
        prompt,
        safety_model,
        sync_together_client,
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=1,
            safety_model=safety_model,
        )

        assert isinstance(response, CompletionResponse)
