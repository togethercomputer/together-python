import os
from unittest.mock import patch

import pytest

from together.client import Together
from together.error import AuthenticationError
from together.types import TogetherClient


class TestTogether:
    @pytest.fixture
    def sync_together_instance(self) -> None:
        """
        Initialize object with mocked API key
        """

        with patch.dict("os.environ", {"TOGETHER_API_KEY": "fake_api_key"}, clear=True):
            return Together()

    def test_init_with_api_key(self, sync_together_instance):
        """
        Test API key from environment works
        """
        assert sync_together_instance.client.api_key == "fake_api_key"

    def test_init_without_api_key(self):
        """
        Test init without API key raises AuthenticationError
        """

        with patch.dict(os.environ, {"TOGETHER_API_KEY": ""}, clear=True):
            with pytest.raises(AuthenticationError):
                Together()

    def test_init_with_base_url_from_env(self):
        """
        Test base_url from environment
        """

        with patch.dict("os.environ", {"TOGETHER_BASE_URL": "https://example.com"}):
            sync_together = Together(api_key="fake_api_key")

            assert sync_together.client.base_url == "https://example.com/"

    def test_init_with_default_base_url(self):
        """
        Test default base_url
        """

        with patch.dict("os.environ", clear=True):
            sync_together = Together(api_key="fake_api_key")

            assert sync_together.client.base_url == "https://api.together.xyz/v1/"

    def test_init_with_supplied_headers(self):
        """
        Test initializing with supplied_headers
        """

        supplied_headers = {"header1": "value1", "header2": "value2"}

        sync_together = Together(api_key="fake_api_key", supplied_headers=supplied_headers)

        assert sync_together.client.supplied_headers == supplied_headers

    def test_completions_initialized(self, sync_together_instance):
        """
        Test initializing completions
        """

        assert sync_together_instance.completions is not None

        assert isinstance(sync_together_instance.completions._client, TogetherClient)

    def test_chat_initialized(self, sync_together_instance):
        """
        Test initializing chat
        """

        assert sync_together_instance.chat is not None

        assert isinstance(sync_together_instance.chat._client, TogetherClient)

        assert isinstance(sync_together_instance.chat.completions._client, TogetherClient)

    def test_embeddings_initialized(self, sync_together_instance):
        """
        Test initializing embeddings
        """

        assert sync_together_instance.embeddings is not None

        assert isinstance(sync_together_instance.embeddings._client, TogetherClient)

    def test_files_initialized(self, sync_together_instance):
        """
        Test initializing files
        """

        assert sync_together_instance.files is not None

        assert isinstance(sync_together_instance.files._client, TogetherClient)

    def test_fine_tuning_initialized(self, sync_together_instance):
        """
        Test initializing fine_tuning
        """

        assert sync_together_instance.fine_tuning is not None

        assert isinstance(sync_together_instance.fine_tuning._client, TogetherClient)

    def test_rerank_initialized(self, sync_together_instance):
        """
        Test initializing rerank
        """

        assert sync_together_instance.rerank is not None

        assert isinstance(sync_together_instance.rerank._client, TogetherClient)
