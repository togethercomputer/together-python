from typing import Any, Dict, Optional, Union, List
import concurrent.futures

import together
from together.utils import create_post_request, get_logger


logger = get_logger(str(__name__))


class embeddings:
    @classmethod
    def create(
        cls,
        input: Union[str, List[str]],
        model: Optional[str] = "",
    ) -> Dict[str, Any]:

        if model == "":
            model = together.default_embedding_model

        if isinstance(input, str):

            parameter_payload = {
                "input": input,
                "model": model,
            }

            return cls._process_input(parameter_payload)

        elif isinstance(input, list):

            response = {"object":"list","data":[],"model":model,"request_id":""}

            # If input is a list, process each string concurrently
            with concurrent.futures.ThreadPoolExecutor() as executor:
                parameter_payloads = [
                    {"input": item, "model": model} for item in input
                ]
                results = list(executor.map(cls._process_input, parameter_payloads))

            response["data"] = [r["data"][0] for r in results]
            response["request_id"] = results[-1]["request_id"]

            return response

    @classmethod
    def _process_input(cls, parameter_payload: Dict[str, Any]) -> Dict[str, Any]:

        # send request
        response = create_post_request(
            url=together.api_base_embeddings, json=parameter_payload
        )

        # return the json as a dictionary
        try:
            response_json = dict(response.json())
        except Exception as e:
            raise together.JSONError(e, http_status=response.status_code)

        return response_json


