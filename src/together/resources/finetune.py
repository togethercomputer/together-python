from together.abstract import api_requestor
from together.downloadmanager import DownloadManager
from together.together_response import TogetherResponse
from together.types import (
    FinetuneList,
    FinetuneListEvents,
    FinetuneRequest,
    FinetuneResponse,
    TogetherClient,
)


class FineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    def create(
        self,
        training_file: str,
        model: str,
        n_epochs: int = 1,
        n_checkpoints: int | None = 1,
        batch_size: int | None = 32,
        learning_rate: float = 0.00001,
        suffix: str | None = None,
        wandb_api_key: str | None = None,
    ) -> FinetuneResponse:
        parameter_payload = FinetuneRequest(
            model=model,
            training_file=training_file,
            n_epochs=n_epochs,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
        ).model_dump()

        response, _, _ = self.requestor.request(
            method="POST",
            url="/fine-tunes",
            params=parameter_payload,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    def list(self) -> FinetuneList:
        response, _, _ = self.requestor.request(
            method="GET",
            url="/fine-tunes",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneList(**response.data)

    def retrieve(self, id: str) -> FinetuneResponse:
        response, _, _ = self.requestor.request(
            method="GET",
            url=f"/fine-tunes/{id}",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    def cancel(self, id: str) -> FinetuneResponse:
        response, _, _ = self.requestor.request(
            method="POST",
            url=f"/fine-tunes/{id}/cancel",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    def list_events(self, id: str) -> FinetuneListEvents:
        response, _, _ = self.requestor.request(
            method="GET",
            url=f"/fine-tunes/{id}/events",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneListEvents(**response.data)

    def download(
        self, id: str, output: str | None = None, checkpoint_step: int = -1
    ) -> str:
        url = f"/finetune/download?ft_id={id}"

        if checkpoint_step > 0:
            url += f"&checkpoint_step={checkpoint_step}"

        remote_name = self.retrieve(id).output_name

        download_manager = DownloadManager(self._client)

        downloaded_filename = download_manager.download(url, output, remote_name)

        return downloaded_filename


class AsyncFineTuning:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    async def create(
        self,
        training_file: str,
        model: str,
        n_epochs: int = 1,
        n_checkpoints: int | None = 1,
        batch_size: int | None = 32,
        learning_rate: float = 0.00001,
        suffix: str | None = None,
        wandb_api_key: str | None = None,
    ) -> FinetuneResponse:
        parameter_payload = FinetuneRequest(
            model=model,
            training_file=training_file,
            n_epochs=n_epochs,
            n_checkpoints=n_checkpoints,
            batch_size=batch_size,
            learning_rate=learning_rate,
            suffix=suffix,
            wandb_api_key=wandb_api_key,
        ).model_dump()

        response, _, _ = await self.requestor.arequest(
            method="POST",
            url="/fine-tunes",
            params=parameter_payload,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    async def list(self) -> FinetuneList:
        response, _, _ = await self.requestor.arequest(
            method="GET",
            url="/fine-tunes",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneList(**response.data)

    async def retrieve(self, id: str) -> FinetuneResponse:
        response, _, _ = await self.requestor.arequest(
            method="GET",
            url=f"/fine-tunes/{id}",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    async def cancel(self, id: str) -> FinetuneResponse:
        response, _, _ = await self.requestor.arequest(
            method="POST",
            url=f"/fine-tunes/{id}/cancel",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneResponse(**response.data)

    async def list_events(self, id: str) -> FinetuneListEvents:
        response, _, _ = await self.requestor.arequest(
            method="GET",
            url=f"/fine-tunes/{id}/events",
            params=None,
            stream=False,
        )

        assert isinstance(response, TogetherResponse)
        return FinetuneListEvents(**response.data)

    async def download(
        self, id: str, output: str | None = None, checkpoint_step: int = -1
    ) -> str:
        raise NotImplementedError(
            "AsyncFineTuning.download not implemented. "
            "Please use FineTuning.download function instead."
        )
