# AudioSpeechRequestVoice

The voice to use for generating the audio. [View all supported voices here](https://docs.together.ai/docs/text-to-speech#voices-available).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.audio_speech_request_voice import AudioSpeechRequestVoice

# TODO update the JSON string below
json = "{}"
# create an instance of AudioSpeechRequestVoice from a JSON string
audio_speech_request_voice_instance = AudioSpeechRequestVoice.from_json(json)
# print the JSON string representation of the object
print(AudioSpeechRequestVoice.to_json())

# convert the object into a dict
audio_speech_request_voice_dict = audio_speech_request_voice_instance.to_dict()
# create an instance of AudioSpeechRequestVoice from a dict
audio_speech_request_voice_from_dict = AudioSpeechRequestVoice.from_dict(audio_speech_request_voice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
