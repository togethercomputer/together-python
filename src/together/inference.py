import os
import urllib.parse
from typing import Any, Dict, Optional, Union

import requests
import sseclient
import json

from together.utils import exit_1, get_logger


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
        stream: Optional[bool] = True,
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

        self.stream = stream

    def inference(
        self,
        prompt: str,
    ) -> Union[Dict[str, Any], requests.Response]:
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
                "stream_tokens": self.stream
            }
        elif self.task == "text2img":
            self.stream = False
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
                self.endpoint_url, headers=headers, json=parameter_payload, stream=self.stream
            )
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        if not self.stream:
            try:
                response_json = dict(response.json())
            except Exception as e:
                self.logger.critical(
                    f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
                )
                exit_1(self.logger)
            return True, response_json

        if response.status_code == 200:
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != '[DONE]':
                    print(json.loads(event.data)['choices'][0]['text'], end="", flush=True),
            print("\n")
            return False, None
        elif response.status_code == 429:
            return True, {"error": "Returned error: no instance"}
        else:
            self.logger.critical(
                    f"Unknown error raised: {e}\nResponse status code = {response.status_code}"
                )
            exit_1(self.logger)
