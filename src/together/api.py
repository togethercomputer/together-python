import json
import os
import urllib.parse
from typing import Optional

import requests

from together.files import Files
from together.finetune import Finetune
from together.inference import Inference


def dispatch_api(args) -> None:
    api = API()
    if args.api == "list-models":
        if args.all:
            api.print_all_models()
        else:
            api.print_available_models()
    elif args.api == "get-raw-supply":
        response = api.get_supply()
        print(json.dumps(response))


class API:
    def __init__(
        self,
        together_api_key: Optional[str] = os.environ.get("TOGETHER_API_KEY", None),
        endpoint_url: Optional[str] = "https://api.together.xyz/",
    ) -> None:
        if together_api_key is None:
            raise Exception("TOGETHER_API_KEY not found. Please set it as an environment variable or using `--key`.")

        self.together_api_key = together_api_key
        self.endpoint_url = endpoint_url

    def get_supply(self) -> dict:
        model_list_endpoint = "https://computer.together.xyz"
        response = requests.get(
            model_list_endpoint,
            json={
                "method": "together_getDepth",
                "id": 1,
            },
        ).json()

        return response

    def print_all_models(self) -> None:
        model_names = self.get_supply()["result"].keys()

        model_names = [sub[:-1] for sub in model_names]  # remove the ? after the model names
        for name in model_names:
            print(name)

    def print_available_models(self) -> None:
        res = self.get_supply()
        names = res["result"].keys()
        available_models = [name[:-1] for name in names if res["result"][name]["num_asks"] > 0]

        for model_name in available_models:
            print(model_name)

    def finetune(self):
        return Finetune(
            self.together_api_key,
            endpoint_url=urllib.parse.urljoin(self.endpoint_url, "/v1/fine-tunes/"),
        )

    def complete(self, **model_kwargs):
        return Inference(
            self.together_api_key,
            endpoint_url=urllib.parse.urljoin(self.endpoint_url, "/api/inference"),
            **model_kwargs,
        )

    def files(self):
        return Files(
            self.together_api_key,
            endpoint_url=urllib.parse.urljoin(self.endpoint_url, "/v1/files/"),
        )
