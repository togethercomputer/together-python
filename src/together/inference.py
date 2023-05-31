import re
import urllib.parse
from typing import List, Optional

import requests


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


def dispatch_inference(args) -> None:
    inference = Inference(
        args.key,
        # endpoint_url=,
        task=args.task,
        model=args.model,
        max_tokens=args.max_tokens,
        # stop_word= args.stop_word,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        repetition_penalty=args.repetition_penalty,
        logprobs=args.logprobs,
    )

    response = inference.inference(args.prompt, stop=args.stop_words)
    print(response)


class Inference:
    def __init__(
        self,
        together_api_key: str = None,
        endpoint_url: Optional[str] = "https://api.together.xyz/",
        task: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = 128,
        # stop_word: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        logprobs: Optional[int] = None,
        # TODO stream_tokens: Optional[bool] = None
    ) -> None:
        self.together_api_key = together_api_key
        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/api/inference")
        self.task = task
        self.model = model
        self.max_tokens = max_tokens
        # self.stop_word = stop_word
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty
        self.logprobs = logprobs

    def inference(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
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
            response = requests.post(self.endpoint_url, headers=headers, json=parameter_payload)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by inference endpoint: {e}")

        generated_text = response.json()

        # TODO Add exception when generated_text has error, See together docs

        try:
            text = generated_text["output"]["choices"][0]["text"]
        except Exception as e:
            raise ValueError(f"Error raised: {e}")

        if stop is not None:
            # TODO remove this and permanently implement api stop_word
            text = _enforce_stop_tokens(text, stop)

        return text
