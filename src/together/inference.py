import base64
import os
import re
import urllib.parse
from typing import Dict, List, Optional, Union

import requests


DEFAULT_ENDPOINT = "https://api.together.xyz/"


def _enforce_stop_tokens(text: str, stop: List[str]) -> str:
    """Cut off the text as soon as any stop words occur."""
    return re.split("|".join(stop), text)[0]


class Inference:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        task: Optional[str] = "text2text",
        model: Optional[str] = None,
        max_tokens: Optional[int] = 128,
        # stop_word: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        logprobs: Optional[int] = None,
        raw: Optional[bool] = False,
        # TODO stream_tokens: Optional[bool] = None
        steps: Optional[int] = 50,
        seed: Optional[int] = 42,
        results: Optional[int] = 1,
        output: Optional[str] = "text2img",
    ) -> None:
        together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if together_api_key is None:
            raise Exception(
                "TOGETHER_API_KEY not found. Please set it as an environment variable"
            )

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        self.together_api_key = together_api_key
        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/api/inference")

        if self.endpoint_url is None:
            raise Exception("Error: Invalid endpoint URL provided.")

        self.task = task
        self.model = model
        self.max_tokens = max_tokens
        # self.stop_word = stop_word
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty
        self.logprobs = logprobs

        # text2img arguments
        self.steps = steps
        self.seed = seed
        self.results = results
        self.output_file_name = output

    def inference(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        raw: Optional[bool] = False,
    ) -> Union[str, Dict[str, str]]:
        if self.task == "text2text":
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
        elif self.task == "text2img":
            parameter_payload = {
                "model": self.model,
                "prompt": prompt,
                "n": self.results,
                "mode": self.task,
                "steps": self.steps,
                "seed": self.seed,
            }
        else:
            raise ValueError("Invalid task supplied")

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

        response_json = dict(response.json())

        if raw:
            return response_json

        if self.task == "text2text":
            # TODO Add exception when generated_text has error, See together docs
            try:
                text = str(response_json["output"]["choices"][0]["text"])
            except Exception as e:
                raise ValueError(f"Error raised: {e}")

            if stop is not None:
                # TODO remove this and permanently implement api stop_word
                text = _enforce_stop_tokens(text, stop)

            return_text = text
        elif self.task == "text2img":
            try:
                images = response_json["output"]["choices"]

                for i in range(len(images)):
                    with open(f"{self.output_file_name}-{i}.png", "wb") as f:
                        f.write(base64.b64decode(images[i]["image_base64"]))
            except (
                requests.exceptions.RequestException
            ) as e:  # This is the correct syntax
                raise ValueError(f"Unknown error raised: {e}")

            return_text = f"Output images saved to {self.output_file_name}-X.png"
        else:
            raise ValueError("Invalid task supplied")

        return return_text
