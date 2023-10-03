from typing import Any, Dict, Optional

import together
from together.utils import create_post_request, get_logger, response_to_dict


logger = get_logger(str(__name__))


class Image:
    @classmethod
    def create(
        self,
        prompt: str,
        model: Optional[str] = "",
        steps: Optional[int] = 20,
        seed: Optional[int] = 42,
        results: Optional[int] = 1,
        height: Optional[int] = 256,
        width: Optional[int] = 256,
        negative_prompt: Optional[str] = "",
    ) -> Dict[str, Any]:
        if model == "":
            model = together.default_image_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "n": results,
            "mode": "text2img",
            "steps": steps,
            "seed": seed,
            "height": height,
            "width": width,
            "negative_prompt": negative_prompt,
        }

        # send request
        response = create_post_request(
            together.api_base_complete, json=parameter_payload
        )

        return response_to_dict(response)
