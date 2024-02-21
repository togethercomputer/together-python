from together import resources
from together.error import TogetherException
from together.version import VERSION
from together._constants import TIMEOUT_SECS, MAX_CONNECTION_RETRIES

import os
from typing import Union, Optional, Dict, Mapping


class Together:
    completions: resources.Completions
    # chat: resources.Chat
    # embeddings: resources.Embeddings
    # files: resources.Files
    # images: resources.Images
    # audio: resources.Audio
    # models: resources.Models
    # fine_tuning: resources.FineTuning

    # client options
    api_key: str
    base_url: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: Union[float, None] = TIMEOUT_SECS,
        max_retries: int = MAX_CONNECTION_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous together client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TOGETHER_API_KEY`
        - `base_url` from `TOGETHER_BASE_URL`
        """
        if api_key is None:
            api_key = os.environ.get("TOGETHER_API_KEY")
        if api_key is None:
            raise TogetherException(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "TOGETHER_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("TOGETHER_BASE_URL")
        if base_url is None:
            base_url = f"https://api.together.xyz/v1"

        self.base_url = base_url

        kwargs = {
            "api_key": api_key,
            "base_url": base_url,
            "timeout": timeout,
            "max_retries": max_retries,
            "default_headers": default_headers,
        }

        self.completions = resources.Completions(**kwargs)
        # self.chat = resources.Chat(self)
        # self.embeddings = resources.Embeddings(self)
        # self.files = resources.Files(self)
        # self.images = resources.Images(self)
        # self.audio = resources.Audio(self)
        # self.models = resources.Models(self)
        # self.fine_tuning = resources.FineTuning(self)


class AsyncTogether:
    completions: resources.AsyncCompletions
    # chat: resources.AsyncChat
    # embeddings: resources.AsyncEmbeddings
    # files: resources.AsyncFiles
    # images: resources.AsyncImages
    # audio: resources.AsyncAudio
    # models: resources.AsyncModels
    # fine_tuning: resources.AsyncFineTuning

    # client options
    api_key: str
    base_url: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: Union[float, None] = TIMEOUT_SECS,
        max_retries: int = MAX_CONNECTION_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async together client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `TOGETHER_API_KEY`
        - `base_url` from `TOGETHER_BASE_URL`
        """
        if api_key is None:
            api_key = os.environ.get("TOGETHER_API_KEY")
        if api_key is None:
            raise TogetherException(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "TOGETHER_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("TOGETHER_BASE_URL")
        if base_url is None:
            base_url = f"https://api.together.xyz/v1"

        self.base_url = base_url

        self.completions = resources.AsyncCompletions()
        # self.chat = resources.AsyncChat(self)
        # self.embeddings = resources.AsyncEmbeddings(self)
        # self.files = resources.AsyncFiles(self)
        # self.images = resources.AsyncImages(self)
        # self.audio = resources.AsyncAudio(self)
        # self.models = resources.AsyncModels(self)
        # self.fine_tuning = resources.AsyncFineTuning(self)


Client = Together
AsyncClient = AsyncTogether
