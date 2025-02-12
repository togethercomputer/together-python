from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Literal, Optional

from together.generated.api.endpoints_api import EndpointsApi
from together.generated.api_client import ApiClient
from together.generated.configuration import Configuration
from together.generated.models.autoscaling import Autoscaling
from together.generated.models.create_endpoint_request import CreateEndpointRequest
from together.generated.models.dedicated_endpoint import DedicatedEndpoint
from together.generated.models.list_endpoint import ListEndpoint
from together.generated.models.update_endpoint_request import UpdateEndpointRequest
from together.types import TogetherClient


class BaseEndpoints:
    """Base class containing common endpoint functionality and documentation."""

    def _get_api_client(self, client: TogetherClient) -> tuple[ApiClient, EndpointsApi]:
        api_client = ApiClient(
            configuration=Configuration(
                host=client.base_url.rstrip("/") if client.base_url else "",
            ),
            header_name="Authorization",
            header_value=f"Bearer {client.api_key}" if client.api_key else None,
        )
        return api_client, EndpointsApi(api_client)


class Endpoints(BaseEndpoints):
    """Synchronous endpoints client."""

    def __init__(self, client: TogetherClient) -> None:
        self.api_client, self._api = self._get_api_client(client)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def __del__(self):
        if hasattr(self, "api_client"):
            self._loop.run_until_complete(self.api_client.close())
            self._loop.close()

    def create(
        self,
        *,
        model: str,
        hardware: str,
        min_replicas: int,
        max_replicas: int,
        display_name: Optional[str] = None,
        disable_prompt_cache: bool = False,
        disable_speculative_decoding: bool = False,
        state: Literal["STARTED", "STOPPED"] = "STARTED",
    ) -> DedicatedEndpoint:
        """
        Create a new dedicated endpoint.

        Args:
            model (str): The model to deploy on this endpoint
            hardware (str): The hardware configuration to use for this endpoint
            min_replicas (int): The minimum number of replicas to maintain
            max_replicas (int): The maximum number of replicas to scale up to
            display_name (str, optional): A human-readable name for the endpoint
            disable_prompt_cache (bool, optional): Whether to disable the prompt cache. Defaults to False.
            disable_speculative_decoding (bool, optional): Whether to disable speculative decoding. Defaults to False.
            state (str, optional): The desired state of the endpoint. Defaults to "STARTED".

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """

        async def _create():
            request = CreateEndpointRequest(
                model=model,
                hardware=hardware,
                autoscaling=Autoscaling(min_replicas=min_replicas, max_replicas=max_replicas),
                display_name=display_name,
                disable_prompt_cache=disable_prompt_cache,
                disable_speculative_decoding=disable_speculative_decoding,
                state=state,
            )
            return await self._api.create_endpoint(create_endpoint_request=request)

        return self._loop.run_until_complete(_create())

    def list(self, type: Literal["dedicated", "serverless"] | None = None) -> List[ListEndpoint]:
        """
        List all endpoints.

        Args:
            type (str, optional): Filter endpoints by type ("dedicated" or "serverless"). Defaults to None.

        Returns:
            Dict[str, Any]: Response containing list of endpoints in the data field
        """

        async def _list():
            return await self._api.list_endpoints(type=type)

        response = self._loop.run_until_complete(_list())
        return response.data

    def get(self, endpoint_id: str) -> DedicatedEndpoint:
        """
        Get details of a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to retrieve

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """

        async def _get():
            return await self._api.get_endpoint(endpoint_id=endpoint_id)

        return self._loop.run_until_complete(_get())

    def delete(self, endpoint_id: str) -> None:
        """
        Delete a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to delete
        """

        async def _delete():
            return await self._api.delete_endpoint(endpoint_id=endpoint_id)

        return self._loop.run_until_complete(_delete())

    def update(
        self,
        endpoint_id: str,
        *,
        min_replicas: Optional[int] = None,
        max_replicas: Optional[int] = None,
        state: Optional[Literal["STARTED", "STOPPED"]] = None,
        display_name: Optional[str] = None,
    ) -> DedicatedEndpoint:
        """
        Update an endpoint's configuration.

        Args:
            endpoint_id (str): ID of the endpoint to update
            min_replicas (int, optional): The minimum number of replicas to maintain
            max_replicas (int, optional): The maximum number of replicas to scale up to
            state (str, optional): The desired state of the endpoint ("STARTED" or "STOPPED")
            display_name (str, optional): A human-readable name for the endpoint

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """

        async def _update():
            kwargs: Dict[str, Any] = {}
            if min_replicas is not None or max_replicas is not None:
                current_min = min_replicas
                current_max = max_replicas
                if current_min is None or current_max is None:
                    # Get current values if only one is specified
                    current = await self._api.get_endpoint(endpoint_id=endpoint_id)
                    current_min = current_min or current.autoscaling.min_replicas
                    current_max = current_max or current.autoscaling.max_replicas
                kwargs["autoscaling"] = Autoscaling(
                    min_replicas=current_min,
                    max_replicas=current_max,
                )
            if state is not None:
                kwargs["state"] = state
            if display_name is not None:
                kwargs["display_name"] = display_name

            request = UpdateEndpointRequest(**kwargs)
            return await self._api.update_endpoint(
                endpoint_id=endpoint_id, update_endpoint_request=request
            )

        return self._loop.run_until_complete(_update())


class AsyncEndpoints(BaseEndpoints):
    """Asynchronous endpoints client."""

    def __init__(self, client: TogetherClient) -> None:
        self.api_client, self._api = self._get_api_client(client)

    async def create(
        self,
        *,
        model: str,
        hardware: str,
        min_replicas: int,
        max_replicas: int,
        display_name: Optional[str] = None,
        disable_prompt_cache: bool = False,
        disable_speculative_decoding: bool = False,
        state: Literal["STARTED", "STOPPED"] = "STARTED",
    ) -> DedicatedEndpoint:
        """
        Create a new dedicated endpoint.

        Args:
            model (str): The model to deploy on this endpoint
            hardware (str): The hardware configuration to use for this endpoint
            min_replicas (int): The minimum number of replicas to maintain
            max_replicas (int): The maximum number of replicas to scale up to
            display_name (str, optional): A human-readable name for the endpoint
            disable_prompt_cache (bool, optional): Whether to disable the prompt cache. Defaults to False.
            disable_speculative_decoding (bool, optional): Whether to disable speculative decoding. Defaults to False.
            state (str, optional): The desired state of the endpoint. Defaults to "STARTED".

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        request = CreateEndpointRequest(
            model=model,
            hardware=hardware,
            autoscaling=Autoscaling(min_replicas=min_replicas, max_replicas=max_replicas),
            display_name=display_name,
            disable_prompt_cache=disable_prompt_cache,
            disable_speculative_decoding=disable_speculative_decoding,
            state=state,
        )
        return await self._api.create_endpoint(create_endpoint_request=request)

    async def list(
        self, type: Literal["dedicated", "serverless"] | None = None
    ) -> List[ListEndpoint]:
        """
        List all endpoints.

        Args:
            type (str, optional): Filter endpoints by type ("dedicated" or "serverless"). Defaults to None.

        Returns:
            Dict[str, Any]: Response containing list of endpoints in the data field
        """
        response = await self._api.list_endpoints(type=type)
        return response.data

    async def get(self, endpoint_id: str) -> DedicatedEndpoint:
        """
        Get details of a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to retrieve

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        return await self._api.get_endpoint(endpoint_id=endpoint_id)

    async def delete(self, endpoint_id: str) -> None:
        """
        Delete a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to delete
        """
        return await self._api.delete_endpoint(endpoint_id=endpoint_id)

    async def update(
        self,
        endpoint_id: str,
        *,
        min_replicas: Optional[int] = None,
        max_replicas: Optional[int] = None,
        state: Optional[Literal["STARTED", "STOPPED"]] = None,
        display_name: Optional[str] = None,
    ) -> DedicatedEndpoint:
        """
        Update an endpoint's configuration.

        Args:
            endpoint_id (str): ID of the endpoint to update
            min_replicas (int, optional): The minimum number of replicas to maintain
            max_replicas (int, optional): The maximum number of replicas to scale up to
            state (str, optional): The desired state of the endpoint ("STARTED" or "STOPPED")
            display_name (str, optional): A human-readable name for the endpoint

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        kwargs: Dict[str, Any] = {}
        if min_replicas is not None or max_replicas is not None:
            current_min = min_replicas
            current_max = max_replicas
            if current_min is None or current_max is None:
                # Get current values if only one is specified
                current = await self._api.get_endpoint(endpoint_id=endpoint_id)
                current_min = current_min or current.autoscaling.min_replicas
                current_max = current_max or current.autoscaling.max_replicas
            kwargs["autoscaling"] = Autoscaling(
                min_replicas=current_min,
                max_replicas=current_max,
            )
        if state is not None:
            kwargs["state"] = state
        if display_name is not None:
            kwargs["display_name"] = display_name

        request = UpdateEndpointRequest(**kwargs)
        return await self._api.update_endpoint(
            endpoint_id=endpoint_id, update_endpoint_request=request
        )
