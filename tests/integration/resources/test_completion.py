import os
from itertools import product

import pytest

from together.client import Together
from together.error import InvalidRequestError
from together.types import CompletionResponse
from together.types.common import ObjectType, UsageData
from together.types.completions import CompletionChoicesData

from ..constants import (
    completion_prompt_list,
    completion_test_model_list,
    moderation_test_model_list,
)
from .generate_hyperparameters import (
    random_frequency_penalty,  # noqa
    random_max_tokens,  # noqa
    random_min_p,  # noqa
    random_presence_penalty,  # noqa
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

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, completion_prompt_list),
    )
    def test_create(
        self,
        model,
        prompt,
        sync_together_client,
        random_max_tokens,  # noqa
        random_temperature,  # noqa
        random_top_p,  # noqa
        random_top_k,  # noqa
        random_presence_penalty,  # noqa
        random_frequency_penalty,  # noqa
        random_min_p,  # noqa
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

        assert -2 <= random_presence_penalty <= 2

        assert -2 <= random_frequency_penalty <= 2

        assert 0 <= random_min_p <= 1

        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=random_max_tokens,
            temperature=random_temperature,
            top_p=random_top_p,
            top_k=random_top_k,
            presence_penalty=random_presence_penalty,
            frequency_penalty=random_frequency_penalty,
            min_p=random_min_p,
            logit_bias={"1024": 10},
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
        product(completion_test_model_list, completion_prompt_list),
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
        product(completion_test_model_list, completion_prompt_list),
    )
    def test_no_prompt(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(TypeError):
            response = sync_together_client.completions.create(  # noqa
                model=model,
                stop=STOP,
                max_tokens=10,
                echo=True,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, completion_prompt_list),
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
        product(completion_test_model_list, completion_prompt_list),
    )
    def test_no_model(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(TypeError):
            response = sync_together_client.completions.create(  # noqa
                prompt=prompt,
                stop=STOP,
                max_tokens=10,
                echo=True,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, completion_prompt_list),
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
            completion_prompt_list,
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
            response = sync_together_client.completions.create(  # noqa
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=max_tokens,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(completion_test_model_list, completion_prompt_list),
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
        product(completion_test_model_list, completion_prompt_list, [1, 2, 3, 4]),
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
            completion_prompt_list,
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
            response = sync_together_client.completions.create(  # noqa
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
            completion_prompt_list,
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
            response = sync_together_client.completions.create(  # noqa
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
            completion_prompt_list,
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

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_repetition_penalty(
        self,
        model,
        prompt,
        sync_together_client,
        random_repetition_penalty,  # noqa
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            repetition_penalty=random_repetition_penalty,
        )

        assert isinstance(response, CompletionResponse)

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_presence_penalty(
        self,
        model,
        prompt,
        sync_together_client,
        random_presence_penalty,  # noqa
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            presence_penalty=random_presence_penalty,
        )

        assert isinstance(response, CompletionResponse)

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_high_presence_penalty(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(  # noqa
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=10,
                presence_penalty=2.1,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_frequency_penalty(
        self,
        model,
        prompt,
        sync_together_client,
        random_frequency_penalty,  # noqa
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            frequency_penalty=random_frequency_penalty,
        )

        assert isinstance(response, CompletionResponse)

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_high_frequency_penalty(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(  # noqa
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=10,
                frequency_penalty=2.1,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_min_p(
        self,
        model,
        prompt,
        sync_together_client,
        random_min_p,  # noqa
    ):
        response = sync_together_client.completions.create(
            prompt=prompt,
            model=model,
            stop=STOP,
            max_tokens=10,
            min_p=random_min_p,
        )

        assert isinstance(response, CompletionResponse)

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_high_min_p(
        self,
        model,
        prompt,
        sync_together_client,
    ):
        with pytest.raises(InvalidRequestError):
            response = sync_together_client.completions.create(  # noqa
                prompt=prompt,
                model=model,
                stop=STOP,
                max_tokens=10,
                min_p=1.1,
            )

    @pytest.mark.parametrize(
        "model,prompt",
        product(
            completion_test_model_list,
            completion_prompt_list,
        ),
    )
    def test_logit_bias(
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
            logit_bias={"1024": 10},
        )

        assert isinstance(response, CompletionResponse)
