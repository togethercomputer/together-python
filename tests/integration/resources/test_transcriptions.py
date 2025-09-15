import os

import pytest

from together.client import Together
from together.types.audio_speech import (
    AudioTranscriptionResponse,
    AudioTranscriptionVerboseResponse,
)


def validate_diarization_response(response_dict):
    """
    Helper function to validate diarization response structure
    """
    # Validate top-level speaker_segments field
    assert "speaker_segments" in response_dict
    assert isinstance(response_dict["speaker_segments"], list)
    assert len(response_dict["speaker_segments"]) > 0

    # Validate each speaker segment structure
    for segment in response_dict["speaker_segments"]:
        assert "text" in segment
        assert "id" in segment
        assert "speaker_id" in segment
        assert "start" in segment
        assert "end" in segment
        assert "words" in segment

        # Validate nested words in speaker segments
        assert isinstance(segment["words"], list)
        for word in segment["words"]:
            assert "id" in word
            assert "word" in word
            assert "start" in word
            assert "end" in word
            assert "speaker_id" in word

    # Validate top-level words field
    assert "words" in response_dict
    assert isinstance(response_dict["words"], list)
    assert len(response_dict["words"]) > 0

    # Validate each word in top-level words
    for word in response_dict["words"]:
        assert "id" in word
        assert "word" in word
        assert "start" in word
        assert "end" in word
        assert "speaker_id" in word


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
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/test_5s_clip.wav"

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
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/test_5s_clip.wav"

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
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/test_5s_clip.wav"

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
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/test_5s_clip.wav"

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
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/test_5s_clip.wav"

        response = sync_together_client.audio.transcriptions.create(file=audio_url)

        assert isinstance(response, AudioTranscriptionResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

    def test_language_detection_hindi(self, sync_together_client):
        """
        Test language detection with Hindi audio file
        """
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/hindi_audio.wav"

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0
        assert hasattr(response, "language")
        assert response.language == "hi"

    def test_diarization_default(self, sync_together_client):
        """
        Test diarization with default model in verbose JSON format
        """
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/2-speaker-conversation.wav"

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            diarize=True,
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

        # Validate diarization fields
        response_dict = response.model_dump()
        validate_diarization_response(response_dict)

    def test_diarization_nvidia(self, sync_together_client):
        """
        Test diarization with nvidia model in verbose JSON format
        """
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/2-speaker-conversation.wav"

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            diarize=True,
            diarization_model="nvidia",
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

        # Validate diarization fields
        response_dict = response.model_dump()
        validate_diarization_response(response_dict)

    def test_diarization_pyannote(self, sync_together_client):
        """
        Test diarization with pyannote model in verbose JSON format
        """
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/2-speaker-conversation.wav"

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            diarize=True,
            diarization_model="pyannote",
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

        # Validate diarization fields
        response_dict = response.model_dump()
        validate_diarization_response(response_dict)

    def test_no_diarization(self, sync_together_client):
        """
        Test with diarize=false should not have speaker segments
        """
        audio_url = "https://together-public-test-data.s3.us-west-2.amazonaws.com/audio/2-speaker-conversation.wav"

        response = sync_together_client.audio.transcriptions.create(
            file=audio_url,
            model="openai/whisper-large-v3",
            response_format="verbose_json",
            diarize=False,
        )

        assert isinstance(response, AudioTranscriptionVerboseResponse)
        assert isinstance(response.text, str)
        assert len(response.text) > 0

        # Verify no diarization fields
        response_dict = response.model_dump()
        assert response_dict.get("speaker_segments") is None
        assert response_dict.get("words") is None

        # Should still have standard fields
        assert "text" in response_dict
        assert "language" in response_dict
        assert "duration" in response_dict
        assert "segments" in response_dict
