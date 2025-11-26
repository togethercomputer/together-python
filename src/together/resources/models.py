from __future__ import annotations

from typing import List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    ModelObject,
    ModelUploadRequest,
    ModelUploadResponse,
    TogetherClient,
    TogetherRequest,
)


class ModelsBase:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def _filter_dedicated_models(
        self, models: List[ModelObject], dedicated_response: TogetherResponse
    ) -> List[ModelObject]:
        """
        Filter models based on dedicated model response.

        Args:
            models (List[ModelObject]): List of all models
            dedicated_response (TogetherResponse): Response from autoscale models endpoint

        Returns:
            List[ModelObject]: Filtered list of models
        """
        assert isinstance(dedicated_response.data, list)

        # Create a set of dedicated model names for efficient lookup
        dedicated_model_names = {model["name"] for model in dedicated_response.data}

        # Filter models to only include those in dedicated_model_names
        # Note: The model.id from ModelObject matches the name field in the autoscale response
        return [model for model in models if model.id in dedicated_model_names]


class Models(ModelsBase):
    def list(
        self,
        dedicated: bool = False,
    ) -> List[ModelObject]:
        """
        Method to return list of models on the API

        Args:
            dedicated (bool, optional): If True, returns only dedicated models. Defaults to False.

        Returns:
            List[ModelObject]: List of model objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, list)

        models = [ModelObject(**model) for model in response.data]

        if dedicated:
            # Get dedicated models
            dedicated_response, _, _ = requestor.request(
                options=TogetherRequest(
                    method="GET",
                    url="autoscale/models",
                ),
                stream=False,
            )

            models = self._filter_dedicated_models(models, dedicated_response)

        models.sort(key=lambda x: x.id.lower())

        return models

    def upload(
        self,
        *,
        model_name: str,
        model_source: str,
        model_type: str = "model",
        hf_token: str | None = None,
        description: str | None = None,
        base_model: str | None = None,
        lora_model: str | None = None,
    ) -> ModelUploadResponse:
        """
        Upload a custom model or adapter from Hugging Face or S3.

        Args:
            model_name (str): The name to give to your uploaded model
            model_source (str): The source location of the model (Hugging Face repo or S3 path)
            model_type (str, optional): Whether the model is a full model or an adapter. Defaults to "model".
            hf_token (str, optional): Hugging Face token (if uploading from Hugging Face)
            description (str, optional): A description of your model
            base_model (str, optional): The base model to use for an adapter if setting it to run against a serverless pool. Only used for model_type "adapter".
            lora_model (str, optional): The lora pool to use for an adapter if setting it to run against, say, a dedicated pool. Only used for model_type "adapter".

        Returns:
            ModelUploadResponse: Object containing upload job information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data = {
            "model_name": model_name,
            "model_source": model_source,
            "model_type": model_type,
        }

        if hf_token is not None:
            data["hf_token"] = hf_token
        if description is not None:
            data["description"] = description
        if base_model is not None:
            data["base_model"] = base_model
        if lora_model is not None:
            data["lora_model"] = lora_model

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="models",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return ModelUploadResponse.from_api_response(response.data)


class AsyncModels(ModelsBase):
    async def list(
        self,
        dedicated: bool = False,
    ) -> List[ModelObject]:
        """
        Async method to return list of models on API

        Args:
            dedicated (bool, optional): If True, returns only dedicated models. Defaults to False.

        Returns:
            List[ModelObject]: List of model objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, list)

        models = [ModelObject(**model) for model in response.data]

        if dedicated:
            # Get dedicated models
            dedicated_response, _, _ = await requestor.arequest(
                options=TogetherRequest(
                    method="GET",
                    url="autoscale/models",
                ),
                stream=False,
            )

            models = self._filter_dedicated_models(models, dedicated_response)

        models.sort(key=lambda x: x.id.lower())

        return models

    async def upload(
        self,
        *,
        model_name: str,
        model_source: str,
        model_type: str = "model",
        hf_token: str | None = None,
        description: str | None = None,
        base_model: str | None = None,
        lora_model: str | None = None,
    ) -> ModelUploadResponse:
        """
        Upload a custom model or adapter from Hugging Face or S3.

        Args:
            model_name (str): The name to give to your uploaded model
            model_source (str): The source location of the model (Hugging Face repo or S3 path)
            model_type (str, optional): Whether the model is a full model or an adapter. Defaults to "model".
            hf_token (str, optional): Hugging Face token (if uploading from Hugging Face)
            description (str, optional): A description of your model
            base_model (str, optional): The base model to use for an adapter if setting it to run against a serverless pool. Only used for model_type "adapter".
            lora_model (str, optional): The lora pool to use for an adapter if setting it to run against, say, a dedicated pool. Only used for model_type "adapter".

        Returns:
            ModelUploadResponse: Object containing upload job information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data = {
            "model_name": model_name,
            "model_source": model_source,
            "model_type": model_type,
        }

        if hf_token is not None:
            data["hf_token"] = hf_token
        if description is not None:
            data["description"] = description
        if base_model is not None:
            data["base_model"] = base_model
        if lora_model is not None:
            data["lora_model"] = lora_model

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="models",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return ModelUploadResponse.from_api_response(response.data)
