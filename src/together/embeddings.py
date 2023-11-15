from typing import Any, Dict, Optional

import together
from together.utils import create_post_request, get_logger


logger = get_logger(str(__name__))


class Embeddings:
    @classmethod
    def create(
        self,
        input: str,
        model: Optional[str] = "",
    ) -> Dict[str, Any]:
        if model == "":
            model = together.default_embedding_model

        parameter_payload = {
            "input": input,
            "model": model,
        }

        # send request
        response = create_post_request(
            url=together.api_base_embeddings, json=parameter_payload
        )

        try:
            response_json = dict(response.json())

        except Exception as e:
            raise together.JSONError(e, http_status=response.status_code)
        return response_json
