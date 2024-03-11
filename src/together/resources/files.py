from __future__ import annotations

from pathlib import Path

from together.abstract import api_requestor
from together.filemanager import DownloadManager
from together.together_response import TogetherResponse
from together.types import (
    FileDeleteResponse,
    FileDownloadResult,
    FileList,
    FileResponse,
    TogetherClient,
    TogetherRequest,
)
from together.utils import normalize_key


class Files:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def upload(self) -> None:
        raise NotImplementedError()

    def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url="files",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FileList(**response.data)

    def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        print(response.data)

        return FileResponse(**response.data)

    def retrieve_content(
        self, id: str, output: Path | str | None = None
    ) -> FileDownloadResult:
        download_manager = DownloadManager(self._client)

        if isinstance(output, str):
            output = Path(output)

        downloaded_filename, file_size = download_manager.download(
            f"files/{id}/content", output, normalize_key(f"{id}.jsonl")
        )

        return FileDownloadResult(
            object="local",
            id=id,
            filename=downloaded_filename,
            size=file_size,
        )

    def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="DELETE",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FileDeleteResponse(**response.data)


class AsyncFiles:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def upload(self) -> None:
        raise NotImplementedError()

    async def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url="files",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FileList(**response.data)

    async def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="GET",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        print(response.data)

        return FileResponse(**response.data)

    async def retrieve_content(self) -> None:
        raise NotImplementedError()

    async def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=TogetherRequest(
                method="DELETE",
                url=f"files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, TogetherResponse)

        return FileDeleteResponse(**response.data)
