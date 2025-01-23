from pathlib import Path
from together import Together

client = Together(base_url="https://staging.together.xyz/")
speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="cartesia/sonic",
    voice="german reporter woman",
    input="Today is a wonderful day to build something people love!",
    response_format="raw",
    stream=True,
)
response.stream_to_file(speech_file_path)
