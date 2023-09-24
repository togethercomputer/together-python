import urllib.parse
from typing import Any, Dict, List

import requests
from loguru import logger

import together
from together.utils.utils import verify_api_key


class Models:
    def __init__(
        self,
    ) -> None:
        verify_api_key()

    @classmethod
    def list(self) -> List[Any]:
        model_url = urllib.parse.urljoin(together.api_base, "models/info?=")
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }
        try:
            response = requests.get(
                model_url,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_list = list(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

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
                f"Model {model} does not exist. Use together.Models.list() to list available models."
            )

        return dict(info_dict)

    @classmethod
    def instances(self) -> Dict[str, bool]:
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "accept": "application/json",
        }
        try:
            response = requests.get(
                together.api_base_instances,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_dict = response.json()
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return dict(response_dict)

    @classmethod
    def start(self, model: str) -> Dict[str, str]:
        model_url = urllib.parse.urljoin(
            together.api_base_instances, f"start?model={model}"
        )
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "accept": "application/json",
        }
        try:
            response = requests.post(
                model_url,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_dict = response.json()
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return dict(response_dict)

    @classmethod
    def stop(self, model: str) -> Dict[str, str]:
        model_url = urllib.parse.urljoin(
            together.api_base_instances, f"stop?model={model}"
        )
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "accept": "application/json",
        }
        try:
            response = requests.post(
                model_url,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_dict = response.json()
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return dict(response_dict)

    @classmethod
    def ready(self, model: str) -> List[Any]:
        ready_url = urllib.parse.urljoin(together.api_base, "models/info?name=" + model)
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "accept": "application/json",
        }
        try:
            response = requests.get(
                ready_url,
                headers=headers,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_list = response.json()
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return list(response_list)

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
