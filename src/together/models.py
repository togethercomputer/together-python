import urllib.parse
from typing import Any, Dict, List

import together
from together.utils import (
    create_get_request,
    create_post_request,
    get_logger,
    response_to_dict,
)


logger = get_logger(str(__name__))


class Models:
    @classmethod
    def list(self) -> List[Any]:
        model_url = urllib.parse.urljoin(together.api_base, "models/info?=")
        response = create_get_request(model_url)

        try:
            response_list = list(response.json())
        except Exception as e:
            raise together.ResponseError(e, http_status=response.status_code)
        return response_list

    @classmethod
    def info(self, model: str, hidden_keys: List[str] = []) -> Dict[str, Any]:
        """
        Gets info dictionary for model from model list and filters out hidden_keys
        """
        info_dict = next((item for item in self.list() if item["name"] == model), None)

        if info_dict is not None:
            for key in set(hidden_keys):
                info_dict.pop(key, None)
        else:
            raise ValueError(
                f"Unable to access {model}. Check your TOGETHER_API_KEY and use together.Models.list() to list available models."
            )

        return dict(info_dict)

    @classmethod
    def instances(self) -> Dict[str, bool]:
        response = create_get_request(together.api_base_instances)

        return response_to_dict(response)

    @classmethod
    def start(self, model: str) -> Dict[str, str]:
        model_url = urllib.parse.urljoin(
            together.api_base_instances, f"start?model={model}"
        )
        response = create_post_request(model_url)

        return response_to_dict(response)

    @classmethod
    def stop(self, model: str) -> Dict[str, str]:
        model_url = urllib.parse.urljoin(
            together.api_base_instances, f"stop?model={model}"
        )
        response = create_post_request(model_url)

        return response_to_dict(response)

    @classmethod
    def ready(self, model: str) -> List[Any]:
        ready_url = urllib.parse.urljoin(together.api_base, "models/info?name=" + model)
        response = create_get_request(ready_url)

        try:
            response_list = list(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_list

    @classmethod
    def _is_finetune_model(self, model: str) -> bool:
        """
        Return boolean value of whether or not model is supported by the finetuning API
        """
        return bool(self.info(model=model).get("finetuning_supported"))

    @classmethod
    def _param_count(self, model: str) -> int:
        """
        Returns model's parameter count. Returns 0 if not found.
        """

        param_count = self.info(model=model).get("num_parameters")

        if not param_count:
            param_count = 0

        return param_count
