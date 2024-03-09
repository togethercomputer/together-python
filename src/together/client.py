from __future__ import annotations

import os
from typing import Dict

from together import resources
from together.constants import BASE_URL, MAX_CONNECTION_RETRIES, TIMEOUT_SECS
from together.error import AuthenticationError
from together.types import TogetherClient


class Together:
    completions: resources.Completions
    chat: resources.Chat
    embeddings: resources.Embeddings
    files: resources.Files
    # images: resources.Images
    # audio: resources.Audio
    # models: resources.Models
    fine_tuning: resources.FineTuning

    # client options
    client: TogetherClient

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = TIMEOUT_SECS,
        max_retries: int = MAX_CONNECTION_RETRIES,
        supplied_headers: Dict[str, str] | None = None,
    ) -> None:
        """Construct a new synchronous together client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TOGETHER_API_KEY`
        - `base_url` from `TOGETHER_BASE_URL`
        """

        if api_key is None:
            api_key = os.environ.get("TOGETHER_API_KEY")

        if api_key is None:
            raise AuthenticationError(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "TOGETHER_API_KEY environment variable"
            )

        if base_url is None:
            base_url = os.environ.get("TOGETHER_BASE_URL")

        if base_url is None:
            base_url = BASE_URL

        self.client = TogetherClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            supplied_headers=supplied_headers,
        )

        self.completions = resources.Completions(self.client)
        self.chat = resources.Chat(self.client)
        self.embeddings = resources.Embeddings(self.client)
        self.files = resources.Files(self.client)
        # self.images = resources.Images(self)
        # self.audio = resources.Audio(self)
        # self.models = resources.Models(self)
        self.fine_tuning = resources.FineTuning(self.client)


class AsyncTogether:
    completions: resources.AsyncCompletions
    chat: resources.AsyncChat
    embeddings: resources.AsyncEmbeddings
    files: resources.AsyncFiles
    # images: resources.AsyncImages
    # audio: resources.AsyncAudio
    # models: resources.AsyncModels
    fine_tuning: resources.AsyncFineTuning

    # client options
    client: TogetherClient

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = TIMEOUT_SECS,
        max_retries: int = MAX_CONNECTION_RETRIES,
        supplied_headers: Dict[str, str] | None = None,
    ) -> None:
        """Construct a new async together client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TOGETHER_API_KEY`
        - `base_url` from `TOGETHER_BASE_URL`
        """

        if api_key is None:
            api_key = os.environ.get("TOGETHER_API_KEY")

        if api_key is None:
            raise AuthenticationError(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "TOGETHER_API_KEY environment variable"
            )

        if base_url is None:
            base_url = os.environ.get("TOGETHER_BASE_URL")

        if base_url is None:
            base_url = BASE_URL

        self.client = TogetherClient(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            supplied_headers=supplied_headers,
        )

        self.completions = resources.AsyncCompletions(self.client)
        self.chat = resources.AsyncChat(self.client)
        self.embeddings = resources.AsyncEmbeddings(self.client)
        self.files = resources.AsyncFiles(self.client)
        # self.images = resources.AsyncImages(self)
        # self.audio = resources.AsyncAudio(self)
        # self.models = resources.AsyncModels(self)
        self.fine_tuning = resources.AsyncFineTuning(self.client)


Client = Together

AsyncClient = AsyncTogether
