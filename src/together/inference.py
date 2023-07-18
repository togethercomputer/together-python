import json
import os
import urllib.parse
from typing import Any, Dict, Optional

import requests
import sseclient  # type: ignore

from together.utils.utils import exit_1, get_logger


DEFAULT_ENDPOINT = "https://api.together.xyz/"


class Inference:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        log_level: str = "WARNING",
        task: Optional[str] = "text2text",
        model: Optional[str] = None,
        max_tokens: Optional[int] = 128,
        stop: Optional[str] = None,
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
        height: Optional[int] = 512,
        width: Optional[int] = 512,
    ) -> None:
        # Setup logger
        self.logger = get_logger(str(__name__), log_level=log_level)

        together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if together_api_key is None:
            self.logger.critical(
                "TOGETHER_API_KEY not found. Please set it as an environment variable."
            )
            exit_1(self.logger)

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        self.together_api_key = together_api_key
        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/api/inference")

        self.task = task
        self.model = model
        self.max_tokens = max_tokens
        self.stop = stop
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty
        self.logprobs = logprobs

        # text2img arguments
        self.steps = steps
        self.seed = seed
        self.results = results
        self.height = height
        self.width = width

    def inference(
        self,
        prompt: str,
    ) -> Dict[str, Any]:
        if self.task == "text2text":
            parameter_payload = {
                "model": self.model,
                "prompt": prompt,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stop": self.stop,
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
                "height": self.height,
                "width": self.width,
            }
        else:
            self.logger.critical(
                f"Invalid task: {self.task}. Pick from either text2text or text2img."
            )
            exit_1(self.logger)

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=parameter_payload,
            )
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        try:
            response_json = dict(response.json())
        except Exception as e:
            self.logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)
        return response_json

    def streaming_inference(self, prompt: str) -> str:
        parameter_payload = {
            "model": self.model,
            "prompt": prompt,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stop": self.stop,
            "repetition_penalty": self.repetition_penalty,
            "logprobs": self.logprobs,
            "stream_tokens": True,
        }
        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=parameter_payload,
                stream=True,
            )
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        if response.status_code == 200:
            output = ""
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != "[DONE]":
                    text = json.loads(event.data)["choices"][0]["text"]
                    output += text
                    print(text, end="", flush=True),
            print("\n")
        elif response.status_code == 429:
            self.logger.critical(
                f"No running instances for {self.model}. You can start an instance by navigating to the Together Playground at api.together.xyz"
            )
            exit_1(self.logger)
        else:
            self.logger.critical(
                f"Unknown error raised.\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)
        return output
