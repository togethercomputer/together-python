import requests
from typing import Optional, Union, List
import re


def enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


class Inference:
    endpoint_url: str = ""
    """Endpoint URL to use."""
    task: Optional[str] = None
    """Task to call the model with.
    Should be a task that returns `generated_text` or `summary_text`."""
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    # stop_word: Optional[str] = None    # TODO stop_words not working? Using LangChain workaround for now...
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    repetition_penalty: Optional[float] = None
    logprobs: Optional[int] = None

    # TODO test stream
    #   stream_tokens: Optional[bool] = None

    together_api_key: Optional[str] = None

    def inference(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ):
        # endpoint = 'https://staging.together.xyz/api/inference'
        parameter_payload = {
            "model": self.model,
            "prompt": prompt,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            # "stop": self.stop_word,
            "repetition_penalty": self.repetition_penalty,
            "logprobs": self.logprobs,
        }

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json",
        }
        # send request
        try:
            response = requests.post(
                self.endpoint_url, headers=headers, json=parameter_payload
            )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by inference endpoint: {e}")

        generated_text = response.json()

        # TODO Add exception when generated_text has error, See langchain implementation + together docs

        text = generated_text["output"]["choices"][0]["text"]

        if stop is not None:
            # TODO remove this and permanently implement api stop_word
            # stop tokens when making calls to Together.
            text = enforce_stop_tokens(text, stop)
        return text
