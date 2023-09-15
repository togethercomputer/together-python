import urllib.parse
from typing import Any, Dict, List

import requests

import together
from together import get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


class Models:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

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
    def ready(self, model: str) -> Dict[str, str]:
        ready_url = urllib.parse.urljoin(
            together.api_base, "models/info"
        )
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
        
        if response.status_code == 200:
            response_json = response.json()
            for model_dict in response_json:
                if model_dict.get("name") == model:
                    depth_num_asks = model_dict["depth"]["num_asks"]
                    if depth_num_asks > 0:
                        return {"ready":f"model is ready for start, status code:{depth_num_asks}"}
                    else:
                        return {"ready":f"model is not ready for start, status code:{depth_num_asks}"}
            else:
                return {"ready":f"No matching model name found for '{model}'."}
        else:
            return {"ready":f"Error: {response.status_code}"}


