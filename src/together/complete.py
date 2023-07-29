import json
from typing import Any, Dict, Iterator, List, Optional

import requests
import sseclient  # type: ignore

import together
from together import get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


class Complete:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def create(
        self,
        prompt: str,
        model: Optional[str] = "",
        max_tokens: Optional[int] = 128,
        stop: Optional[List[str]] = [],
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        logprobs: Optional[int] = None,
    ) -> Dict[str, Any]:
        if model == "":
            model = together.default_text_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "logprobs": logprobs,
        }

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.post(
                together.api_base_complete,
                headers=headers,
                json=parameter_payload,
            )
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        if response.status_code == 429:
            logger.critical(
                f"No running instances for {model}. You can start an instance by navigating to the Together Playground at api.together.ai"
            )
            raise together.InstanceError(model=model)

        response.raise_for_status()

        try:
            response_json = dict(response.json())

        except Exception as e:
            logger.critical(
                f"Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)
        return response_json

    @classmethod
    def create_streaming(
        self,
        prompt: str,
        model: Optional[str] = "",
        max_tokens: Optional[int] = 128,
        stop: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
    ) -> Iterator[str]:
        """
        Prints streaming responses and returns the completed text.
        """

        if model == "":
            model = together.default_text_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "stream_tokens": True,
        }
        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.post(
                together.api_base_complete,
                headers=headers,
                json=parameter_payload,
                stream=True,
            )
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        if response.status_code == 200:
            output = ""
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != "[DONE]":
                    text = json.loads(event.data)["choices"][0]["text"]
                    output += text
                    yield text
        elif response.status_code == 429:
            logger.critical(
                f"No running instances for {model}. You can start an instance by navigating to the Together Playground at api.together.ai"
            )
            raise together.InstanceError(model=model)
        else:
            logger.critical(
                f"Unknown error raised.\nResponse status code = {response.status_code}"
            )
            response.raise_for_status()
            raise together.ResponseError(http_status=response.status_code)
