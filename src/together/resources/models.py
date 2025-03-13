from __future__ import annotations

from typing import List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    ModelObject,
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
