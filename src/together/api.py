import urllib.parse
from typing import Any, List

import requests

import together
from together.utils.utils import exit_1, get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


class API:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def get_models(self) -> List[Any]:
        model_url = urllib.parse.urljoin(together.api_base, "models/info?=")
        headers = {
            "Authorization": f"Bearer {together.api_key}",
        }
        try:
            response = requests.get(
                model_url,
                headers=headers,
            )
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            exit_1(logger)

        try:
            response_list = list(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(logger)

        return response_list
