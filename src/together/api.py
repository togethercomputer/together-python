import os
import urllib.parse
from typing import Any, List, Optional

import requests

from together.complete import Complete
from together.files import Files
from together.finetune import Finetune
from together.utils.utils import exit_1, get_logger


DEFAULT_ENDPOINT = "https://api.together.xyz/"
DEFAULT_SUPPLY_ENDPOINT = "https://computer.together.xyz"


class API:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        supply_endpoint_url: Optional[str] = None,
        log_level: str = "WARNING",
        api_key: Optional[str] = None,
    ) -> None:
        # Setup logger
        self.logger = get_logger(__name__, log_level=log_level)
        self.log_level = log_level

        if api_key is None:
            self.together_api_key = os.environ.get("TOGETHER_API_KEY", None)
            if self.together_api_key is None:
                self.logger.critical(
                    "TOGETHER_API_KEY not found. Please set it as an environment variable or set it with api_key."
                )
                exit_1(self.logger)
        else:
            self.together_api_key = api_key

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        if supply_endpoint_url is None:
            supply_endpoint_url = DEFAULT_SUPPLY_ENDPOINT

        self.endpoint_url = endpoint_url
        self.supply_endpoint_url = supply_endpoint_url

    def get_models(self) -> List[Any]:
        model_url = urllib.parse.urljoin(self.endpoint_url, "models/info?=")
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }
        try:
            response = requests.get(
                model_url,
                headers=headers,
            )
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        try:
            response_list = list(response.json())
        except Exception as e:
            self.logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)

        return response_list

    def finetune(self) -> Finetune:
        return Finetune(
            endpoint_url=self.endpoint_url,
            log_level=self.log_level,
        )

    def complete(self, **model_kwargs: Any) -> Complete:
        return Complete(
            endpoint_url=self.endpoint_url,
            **model_kwargs,
            log_level=self.log_level,
        )

    def files(self) -> Files:
        return Files(
            endpoint_url=self.endpoint_url,
            log_level=self.log_level,
        )
