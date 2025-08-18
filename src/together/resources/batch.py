from __future__ import annotations

from typing import List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    TogetherClient,
    TogetherRequest,
    BatchJob,
)


class Batches:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def create_batch(self, file_id: str, endpoint: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = {
            "input_file_id": file_id,
            "endpoint": endpoint,
            "completion_window": "24h",
        }

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url=f"batches",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        response_body = response.data.get("job", {})
        return BatchJob(**response_body)

    def get_batch(self, batch_job_id: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"batches/{batch_job_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return BatchJob(**response.data)

    def list_batches(self) -> List[BatchJob]:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="batches",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        jobs = response.data or []
        return [BatchJob(**job) for job in jobs]

    def cancel_batch(self, batch_job_id: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url=f"batches/{batch_job_id}/cancel",
            ),
            stream=False,
        )

        return BatchJob(**response.data)


class AsyncBatches:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create_batch(self, file_id: str, endpoint: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        parameter_payload = {
            "input_file_id": file_id,
            "endpoint": endpoint,
            "completion_window": "24h",
        }

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url=f"batches",
                params=parameter_payload,
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        response_body = response.data.get("job", {})
        return BatchJob(**response_body)

    async def get_batch(self, batch_job_id: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"batches/{batch_job_id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return BatchJob(**response.data)

    async def list_batches(self) -> List[BatchJob]:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="batches",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        jobs = response.data or []
        return [BatchJob(**job) for job in jobs]

    async def cancel_batch(self, batch_job_id: str) -> BatchJob:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="POST",
                url=f"batches/{batch_job_id}/cancel",
            ),
            stream=False,
        )

        return BatchJob(**response.data)
