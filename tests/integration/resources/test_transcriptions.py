import os

import pytest

from together.client import Together
from together.types.audio_speech import (
    AudioTranscriptionResponse,
    AudioTranscriptionVerboseResponse,
)


class TestTogetherTranscriptions:
    @pytest.fixture
    def sync_together_client(self) -> Together:
        """
        Initialize object with API key from environment
        """
        TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
        return Together(api_key=TOGETHER_API_KEY)

    def test_basic_transcription_url(self, sync_together_client):
        """
        Test basic transcription with URL audio file
        """
        audio_url = (
            "https://voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav"
        )

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url, model="openai/whisper-large-v3"
        )

        assert isinstance(response, AudioTranscriptionResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    def test_transcription_with_language(self, sync_together_client):
        """
        Test transcription with language parameter
        """
        audio_url = (
            "https://voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav"
        )

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url, model="openai/whisper-large-v3", language="en"
        )

        assert isinstance(response, AudioTranscriptionResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    def test_transcription_verbose_json(self, sync_together_client):
        """
        Test transcription with verbose JSON format and timestamps
        """
        audio_url = (
            "https://voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav"
        )

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            timestamp_granularities="segment",
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert hasattr(response, "segments")

    def test_transcription_with_temperature(self, sync_together_client):
        """
        Test transcription with temperature parameter
        """
        audio_url = (
            "https://voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav"
        )

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url, model="openai/whisper-large-v3", temperature=0.2
        )

        assert isinstance(response, AudioTranscriptionResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    def test_transcription_missing_file(self, sync_together_client):
        """
        Test transcription with missing file parameter
        """
        with pytest.raises(TypeError):
            sync_together_client.audio.transcriptions.create(
                model="openai/whisper-large-v3"
            )

    def test_transcription_missing_model(self, sync_together_client):
        """
        Test transcription with missing model parameter - should use default model
        """
        audio_url = (
            "https://voiptroubleshooter.com/open_speech/american/OSR_us_000_0010_8k.wav"
        )

        response = sync_together_client.audio.transcriptions.create(file=audio_url)

        assert isinstance(response, AudioTranscriptionResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0
