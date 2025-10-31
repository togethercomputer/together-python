from __future__ import annotations

from typing import Dict, List, Literal, Optional, Union

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import TogetherClient, TogetherRequest
from together.types.endpoints import DedicatedEndpoint, HardwareWithStatus, ListEndpoint


class Endpoints:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def list(
        self,
        type: Optional[Literal["dedicated", "serverless"]] = None,
        usage_type: Optional[Literal["on-demand", "reserved"]] = None,
        mine: Optional[bool] = None,
    ) -> List[ListEndpoint]:
        """
        List all endpoints, can be filtered by endpoint type and ownership.

        Args:
            type (str, optional): Filter endpoints by endpoint type ("dedicated" or "serverless"). Defaults to None.
            usage_type (str, optional): Filter endpoints by usage type ("on-demand" or "reserved"). Defaults to None.
            mine (bool, optional): If True, return only endpoints owned by the caller. Defaults to None.

        Returns:
            List[ListEndpoint]: List of endpoint objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params: Dict[
            str,
            Union[
                Literal["dedicated", "serverless"],
                Literal["on-demand", "reserved"],
                bool,
            ],
        ] = {}
        if type is not None:
            params["type"] = type
        if usage_type is not None:
            params["usage_type"] = usage_type
        if mine is not None:
            params["mine"] = mine

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="endpoints",
                params=params,
            ),
            stream=False,
        )

        response.data = response.data["data"]

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, list)

        return [ListEndpoint(**endpoint) for endpoint in response.data]

    def create(
        self,
        *,
        model: str,
        hardware: str,
        min_replicas: int,
        max_replicas: int,
        display_name: Optional[str] = None,
        disable_prompt_cache: bool = True,
        disable_speculative_decoding: bool = True,
        state: Literal["STARTED", "STOPPED"] = "STARTED",
        inactive_timeout: Optional[int] = None,
        availability_zone: Optional[str] = None,
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
            inactive_timeout (int, optional): The number of minutes of inactivity after which the endpoint will be automatically stopped. Set to 0 to disable automatic timeout.
            availability_zone (str, optional): Start endpoint in specified availability zone (e.g., us-central-4b).

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, Union[str, bool, Dict[str, int], int]] = {
            "model": model,
            "hardware": hardware,
            "autoscaling": {
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
            },
            "disable_prompt_cache": disable_prompt_cache,
            "disable_speculative_decoding": disable_speculative_decoding,
            "state": state,
        }

        if display_name is not None:
            data["display_name"] = display_name

        if inactive_timeout is not None:
            data["inactive_timeout"] = inactive_timeout

        if availability_zone is not None:
            data["availability_zone"] = availability_zone

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="endpoints",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    def get(self, endpoint_id: str) -> DedicatedEndpoint:
        """
        Get details of a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to retrieve

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"endpoints/{endpoint_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    def delete(self, endpoint_id: str) -> None:
        """
        Delete a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to delete
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        requestor.request(
            options=TogetherRequest(
                method="DELETE",
                url=f"endpoints/{endpoint_id}",
            ),
            stream=False,
        )

    def update(
        self,
        endpoint_id: str,
        *,
        min_replicas: Optional[int] = None,
        max_replicas: Optional[int] = None,
        state: Optional[Literal["STARTED", "STOPPED"]] = None,
        display_name: Optional[str] = None,
        inactive_timeout: Optional[int] = None,
    ) -> DedicatedEndpoint:
        """
        Update an endpoint's configuration.

        Args:
            endpoint_id (str): ID of the endpoint to update
            min_replicas (int, optional): The minimum number of replicas to maintain
            max_replicas (int, optional): The maximum number of replicas to scale up to
            state (str, optional): The desired state of the endpoint ("STARTED" or "STOPPED")
            display_name (str, optional): A human-readable name for the endpoint
            inactive_timeout (int, optional): The number of minutes of inactivity after which the endpoint will be automatically stopped. Set to 0 to disable automatic timeout.

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, Union[str, Dict[str, int], int]] = {}

        if min_replicas is not None or max_replicas is not None:
            current_min = min_replicas
            current_max = max_replicas
            if current_min is None or current_max is None:
                # Get current values if only one is specified
                current = self.get(endpoint_id=endpoint_id)
                current_min = current_min or current.autoscaling.min_replicas
                current_max = current_max or current.autoscaling.max_replicas
            data["autoscaling"] = {
                "min_replicas": current_min,
                "max_replicas": current_max,
            }

        if state is not None:
            data["state"] = state

        if display_name is not None:
            data["display_name"] = display_name

        if inactive_timeout is not None:
            data["inactive_timeout"] = inactive_timeout

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="PATCH",
                url=f"endpoints/{endpoint_id}",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    def list_hardware(self, model: Optional[str] = None) -> List[HardwareWithStatus]:
        """
        List available hardware configurations.

        Args:
            model (str, optional): Filter hardware configurations by model compatibility. When provided,
                                 the response includes availability status for each compatible configuration.

        Returns:
            List[HardwareWithStatus]: List of hardware configurations with their status
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params = {}
        if model is not None:
            params["model"] = model

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="hardware",
                params=params,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, dict)
        assert isinstance(response.data["data"], list)

        return [HardwareWithStatus(**item) for item in response.data["data"]]

    def list_avzones(self) -> List[str]:
        """
        List all available availability zones.

        Returns:
            List[str]: List of unique availability zones
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="clusters/availability-zones",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, dict)
        assert isinstance(response.data["avzones"], list)

        return response.data["avzones"]


class AsyncEndpoints:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def list(
        self,
        type: Optional[Literal["dedicated", "serverless"]] = None,
        usage_type: Optional[Literal["on-demand", "reserved"]] = None,
        mine: Optional[bool] = None,
    ) -> List[ListEndpoint]:
        """
        List all endpoints, can be filtered by type and ownership.

        Args:
            type (str, optional): Filter endpoints by type ("dedicated" or "serverless"). Defaults to None.
            usage_type (str, optional): Filter endpoints by usage type ("on-demand" or "reserved"). Defaults to None.
            mine (bool, optional): If True, return only endpoints owned by the caller. Defaults to None.

        Returns:
            List[ListEndpoint]: List of endpoint objects
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params: Dict[
            str,
            Union[
                Literal["dedicated", "serverless"],
                Literal["on-demand", "reserved"],
                bool,
            ],
        ] = {}
        if type is not None:
            params["type"] = type
        if usage_type is not None:
            params["usage_type"] = usage_type
        if mine is not None:
            params["mine"] = mine

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="endpoints",
                params=params,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, list)

        return [ListEndpoint(**endpoint) for endpoint in response.data]

    async def create(
        self,
        *,
        model: str,
        hardware: str,
        min_replicas: int,
        max_replicas: int,
        display_name: Optional[str] = None,
        disable_prompt_cache: bool = True,
        disable_speculative_decoding: bool = True,
        state: Literal["STARTED", "STOPPED"] = "STARTED",
        inactive_timeout: Optional[int] = None,
        availability_zone: Optional[str] = None,
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
            inactive_timeout (int, optional): The number of minutes of inactivity after which the endpoint will be automatically stopped. Set to 0 to disable automatic timeout.

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, Union[str, bool, Dict[str, int], int]] = {
            "model": model,
            "hardware": hardware,
            "autoscaling": {
                "min_replicas": min_replicas,
                "max_replicas": max_replicas,
            },
            "disable_prompt_cache": disable_prompt_cache,
            "disable_speculative_decoding": disable_speculative_decoding,
            "state": state,
        }

        if display_name is not None:
            data["display_name"] = display_name

        if inactive_timeout is not None:
            data["inactive_timeout"] = inactive_timeout

        if availability_zone is not None:
            data["availability_zone"] = availability_zone

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url="endpoints",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    async def get(self, endpoint_id: str) -> DedicatedEndpoint:
        """
        Get details of a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to retrieve

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"endpoints/{endpoint_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    async def delete(self, endpoint_id: str) -> None:
        """
        Delete a specific endpoint.

        Args:
            endpoint_id (str): ID of the endpoint to delete
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        await requestor.arequest(
            options=TogetherRequest(
                method="DELETE",
                url=f"endpoints/{endpoint_id}",
            ),
            stream=False,
        )

    async def update(
        self,
        endpoint_id: str,
        *,
        min_replicas: Optional[int] = None,
        max_replicas: Optional[int] = None,
        state: Optional[Literal["STARTED", "STOPPED"]] = None,
        display_name: Optional[str] = None,
        inactive_timeout: Optional[int] = None,
    ) -> DedicatedEndpoint:
        """
        Update an endpoint's configuration.

        Args:
            endpoint_id (str): ID of the endpoint to update
            min_replicas (int, optional): The minimum number of replicas to maintain
            max_replicas (int, optional): The maximum number of replicas to scale up to
            state (str, optional): The desired state of the endpoint ("STARTED" or "STOPPED")
            display_name (str, optional): A human-readable name for the endpoint
            inactive_timeout (int, optional): The number of minutes of inactivity after which the endpoint will be automatically stopped. Set to 0 to disable automatic timeout.

        Returns:
            DedicatedEndpoint: Object containing endpoint information
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        data: Dict[str, Union[str, Dict[str, int], int]] = {}

        if min_replicas is not None or max_replicas is not None:
            current_min = min_replicas
            current_max = max_replicas
            if current_min is None or current_max is None:
                # Get current values if only one is specified
                current = await self.get(endpoint_id=endpoint_id)
                current_min = current_min or current.autoscaling.min_replicas
                current_max = current_max or current.autoscaling.max_replicas
            data["autoscaling"] = {
                "min_replicas": current_min,
                "max_replicas": current_max,
            }

        if state is not None:
            data["state"] = state

        if display_name is not None:
            data["display_name"] = display_name

        if inactive_timeout is not None:
            data["inactive_timeout"] = inactive_timeout

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="PATCH",
                url=f"endpoints/{endpoint_id}",
                params=data,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return DedicatedEndpoint(**response.data)

    async def list_hardware(
        self, model: Optional[str] = None
    ) -> List[HardwareWithStatus]:
        """
        List available hardware configurations.

        Args:
            model (str, optional): Filter hardware configurations by model compatibility. When provided,
                                 the response includes availability status for each compatible configuration.

        Returns:
            List[HardwareWithStatus]: List of hardware configurations with their status
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        params = {}
        if model is not None:
            params["model"] = model

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="hardware",
                params=params,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, dict)
        assert isinstance(response.data["data"], list)

        return [HardwareWithStatus(**item) for item in response.data["data"]]

    async def list_avzones(self) -> List[str]:
        """
        List all availability zones.

        Returns:
            List[str]: List of unique availability zones
        """
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="clusters/availability-zones",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        assert isinstance(response.data, dict)
        assert isinstance(response.data["avzones"], list)

        return response.data["avzones"]
