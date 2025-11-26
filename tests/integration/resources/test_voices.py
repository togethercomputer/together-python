import os

import pytest

from together.client import AsyncTogether, Together
from together.types.audio_speech import ModelVoices, VoiceListResponse


class TestTogetherVoices:
    @pytest.fixture
    def sync_together_client(self) -> Together:
        """
        Initialize sync client with API key from environment
        """
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        return Together(api_key=TOGETHER_API_KEY)

    @pytest.fixture
    def async_together_client(self) -> AsyncTogether:
        """
        Initialize async client with API key from environment
        """
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        return AsyncTogether(api_key=TOGETHER_API_KEY)

    def test_sync_voices_list(self, sync_together_client):
        """
        Test sync voices list endpoint
        """
        response = sync_together_client.audio.voices.list()

        # Verify response type
        assert isinstance(response, VoiceListResponse)

        # Verify data structure
        assert hasattr(response, "data")
        assert isinstance(response.data, list)
        assert len(response.data) > 0

        # Verify each model has the correct structure
        for model_voices in response.data:
            assert isinstance(model_voices, ModelVoices)
            assert hasattr(model_voices, "model")
            assert isinstance(model_voices.model, str)
            assert len(model_voices.model) > 0
            print(model_voices)
            assert hasattr(model_voices, "voices")
            assert isinstance(model_voices.voices, list)
            assert len(model_voices.voices) > 0

            # Verify each voice has a name
            for voice in model_voices.voices:
                assert isinstance(voice, dict)
                assert "name" in voice
                assert isinstance(voice["name"], str)
                assert len(voice["name"]) > 0

    @pytest.mark.asyncio
    async def test_async_voices_list(self, async_together_client):
        """
        Test async voices list endpoint
        """
        response = await async_together_client.audio.voices.list()

        # Verify response type
        assert isinstance(response, VoiceListResponse)

        # Verify data structure
        assert hasattr(response, "data")
        assert isinstance(response.data, list)
        assert len(response.data) > 0

        # Verify each model has the correct structure
        for model_voices in response.data:
            assert isinstance(model_voices, ModelVoices)
            assert hasattr(model_voices, "model")
            assert isinstance(model_voices.model, str)
            assert len(model_voices.model) > 0
            print(model_voices)
            assert hasattr(model_voices, "voices")
            assert isinstance(model_voices.voices, list)
            assert len(model_voices.voices) > 0

            # Verify each voice has a name
            for voice in model_voices.voices:
                assert isinstance(voice, dict)
                assert "name" in voice
                assert isinstance(voice["name"], str)
                assert len(voice["name"]) > 0

    def test_sync_voices_content(self, sync_together_client):
        """
        Test that sync voices list returns expected models
        """
        response = sync_together_client.audio.voices.list()

        # Get list of model names
        model_names = [model_voices.model for model_voices in response.data]

        # Verify we have at least some known models
        assert len(model_names) > 0

        # Check that each model has at least one voice
        for model_voices in response.data:
            assert len(model_voices.voices) > 0

    @pytest.mark.asyncio
    async def test_async_voices_content(self, async_together_client):
        """
        Test that async voices list returns expected models
        """
        response = await async_together_client.audio.voices.list()

        # Get list of model names
        model_names = [model_voices.model for model_voices in response.data]

        # Verify we have at least some known models
        assert len(model_names) > 0

        # Check that each model has at least one voice
        for model_voices in response.data:
            assert len(model_voices.voices) > 0
