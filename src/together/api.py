import requests
import json
from typing import Optional

from together.inference import Inference
from together.finetune import Finetune
from together.files import Files

import urllib.parse


def dispatch_api(args):
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
        together_api_key: Optional[str],
        endpoint_url: Optional[str] = "https://api.together.xyz/",
    ) -> None:
        self.together_api_key = together_api_key
        self.endpoint_url = endpoint_url

    def get_supply(self):
        model_list_endpoint = "https://computer.together.xyz"
        response = requests.get(
            model_list_endpoint,
            json={
                "method": "together_getDepth",
                "id": 1,
            },
        ).json()

        return response

    def print_all_models(self):
        model_names = self.get_supply()["result"].keys()

        model_names = [
            sub[:-1] for sub in model_names
        ]  # remove the ? after the model names
        for name in model_names:
            print(name)

    def print_available_models(self):
        res = self.get_supply()
        names = res["result"].keys()
        available_models = [
            name[:-1] for name in names if res["result"][name]["num_asks"] > 0
        ]

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
