import os
from typing import Any, Dict, List, Optional, cast

import requests

from together.files import Files
from together.finetune import Finetune
from together.inference import Inference


DEFAULT_ENDPOINT = "https://api.together.xyz/"
DEFAULT_SUPPLY_ENDPOINT = "https://computer.together.xyz"


class API:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        supply_endpoint_url: Optional[str] = None,
    ) -> None:
        self.together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if self.together_api_key is None:
            raise Exception(
                "TOGETHER_API_KEY not found. Please set it as an environment variable."
            )

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        if supply_endpoint_url is None:
            supply_endpoint_url = DEFAULT_SUPPLY_ENDPOINT

        self.endpoint_url = endpoint_url
        self.supply_endpoint_url = supply_endpoint_url

    def get_supply(self) -> Dict[str, Any]:
        try:
            response = requests.get(
                self.supply_endpoint_url,
                json={
                    "method": "together_getDepth",
                    "id": 1,
                },
            )
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def get_all_models(self) -> List[str]:
        models = cast(List[str], self.get_supply()["result"].keys())

        models = [str(sub[:-1]) for sub in models]  # remove the ? after the model names

        return models

    def get_available_models(self) -> List[str]:
        res = self.get_supply()
        names = res["result"].keys()
        available_models = [
            name[:-1] for name in names if res["result"][name]["num_asks"] > 0
        ]

        return available_models

    def finetune(self) -> Finetune:
        return Finetune(
            endpoint_url=self.endpoint_url,
        )

    def complete(self, **model_kwargs: Any) -> Inference:
        return Inference(
            endpoint_url=self.endpoint_url,
            **model_kwargs,
        )

    def files(self) -> Files:
        return Files(
            endpoint_url=self.endpoint_url,
        )
