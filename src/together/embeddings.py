import concurrent.futures
from typing import Any, Dict, List, Optional, Union

import together
from together.utils import create_post_request, get_logger


logger = get_logger(str(__name__))


class DataItem:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding


class EmbeddingsOutput:
    def __init__(self, data: List[DataItem]):
        self.data = data


class Embeddings:
    @classmethod
    def create(
        cls,
        input: Union[str, List[str]],
        model: Optional[str] = "",
    ) -> EmbeddingsOutput:
        if model == "":
            model = together.default_embedding_model

        if isinstance(input, str):
            parameter_payload = {
                "input": input,
                "model": model,
            }

            response = cls._process_input(parameter_payload)

            return EmbeddingsOutput([DataItem(response["data"][0]["embedding"])])

        elif isinstance(input, list):
            # If input is a list, process each string concurrently
            with concurrent.futures.ThreadPoolExecutor() as executor:
                parameter_payloads = [{"input": item, "model": model} for item in input]
                results = list(executor.map(cls._process_input, parameter_payloads))

            return EmbeddingsOutput(
                [DataItem(item["data"][0]["embedding"]) for item in results]
            )

    @classmethod
    def _process_input(cls, parameter_payload: Dict[str, Any]) -> Dict[str, Any]:
        # send request
        response = create_post_request(
            url=together.api_base_embeddings, json=parameter_payload
        )

        # return the json as a DotDict
        try:
            response_json = dict(response.json())
        except Exception as e:
            raise together.JSONError(e, http_status=response.status_code)

        return response_json
