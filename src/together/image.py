import os
import urllib.parse
from typing import Any, Dict, Optional

import requests

from together.utils.utils import exit_1, get_logger


DEFAULT_ENDPOINT = "https://api.together.xyz/"
DEFAULT_IMAGE_MODEL = "runwayml/stable-diffusion-v1-5"


class Image:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        log_level: str = "WARNING",
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

    def create(
        self,
        prompt: str,
        model: Optional[str] = "",
        steps: Optional[int] = 50,
        seed: Optional[int] = 42,
        results: Optional[int] = 1,
        height: Optional[int] = 256,
        width: Optional[int] = 256,
    ) -> Dict[str, Any]:
        if model == "":
            model = DEFAULT_IMAGE_MODEL

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "n": results,
            "mode": "text2img",
            "steps": steps,
            "seed": seed,
            "height": height,
            "width": width,
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
