import os
from unittest.mock import patch

import pytest

from together.client import AsyncTogether
from together.error import AuthenticationError
from together.types import TogetherClient


class TestAsyncTogether:
    @pytest.fixture
    def async_together_instance(self):
        """
        Initialize object with mocked API key
        """
        with patch.dict("os.environ", {"TOGETHER_API_KEY": "fake_api_key"}):
            return AsyncTogether()

    def test_init_with_api_key(self, async_together_instance):
        """
        Test API key from environment works
        """

        assert async_together_instance.client.api_key == "fake_api_key"

    def test_init_without_api_key(self):
        """
        Test API key without API key raises AuthenticationError
        """

        with patch.dict(os.environ, {"TOGETHER_API_KEY": ""}, clear=True):
            with pytest.raises(AuthenticationError):
                AsyncTogether()

    def test_init_with_base_url_from_env(self):
        """
        Test base_url from environment
        """

        with patch.dict("os.environ", {"TOGETHER_BASE_URL": "https://example.com"}):
            async_together = AsyncTogether(api_key="fake_api_key")

            assert async_together.client.base_url == "https://example.com/"

    def test_init_with_default_base_url(self):
        """
        Test default base_url
        """

        async_together = AsyncTogether(api_key="fake_api_key")

        assert async_together.client.base_url == "https://api.together.xyz/v1/"

    def test_init_with_supplied_headers(self):
        """
        Test initializing with supplied_headers
        """

        supplied_headers = {"header1": "value1", "header2": "value2"}

        async_together = AsyncTogether(
            api_key="fake_api_key", supplied_headers=supplied_headers
        )

        assert async_together.client.supplied_headers == supplied_headers

    def test_completions_initialized(self, async_together_instance):
        """
        Test initializing completions
        """

        assert async_together_instance.completions is not None

        assert isinstance(async_together_instance.completions._client, TogetherClient)

    def test_chat_initialized(self, async_together_instance):
        """
        Test initializing chat
        """

        assert async_together_instance.chat is not None

        assert isinstance(async_together_instance.chat._client, TogetherClient)

        assert isinstance(
            async_together_instance.chat.completions._client, TogetherClient
        )

    def test_embeddings_initialized(self, async_together_instance):
        """
        Test initializing embeddings
        """

        assert async_together_instance.embeddings is not None

        assert isinstance(async_together_instance.embeddings._client, TogetherClient)

    def test_files_initialized(self, async_together_instance):
        """
        Test initializing files
        """

        assert async_together_instance.files is not None

        assert isinstance(async_together_instance.files._client, TogetherClient)

    def test_fine_tuning_initialized(self, async_together_instance):
        """
        Test initializing fine_tuning
        """

        assert async_together_instance.fine_tuning is not None

        assert isinstance(async_together_instance.fine_tuning._client, TogetherClient)

    def test_rerank_initialized(self, async_together_instance):
        """
        Test initializing rerank
        """

        assert async_together_instance.rerank is not None

        assert isinstance(async_together_instance.rerank._client, TogetherClient)
