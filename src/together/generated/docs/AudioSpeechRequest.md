# AudioSpeechRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | [**AudioSpeechRequestModel**](AudioSpeechRequestModel.md) |  |
**input** | **str** | Input text to generate the audio for |
**voice** | [**AudioSpeechRequestVoice**](AudioSpeechRequestVoice.md) |  |
**response_format** | **str** | The format of audio output | [optional] [default to 'wav']
**language** | **str** | Language of input text | [optional] [default to 'en']
**response_encoding** | **str** | Audio encoding of response | [optional] [default to 'pcm_f32le']
**sample_rate** | **float** | Sampling rate to use for the output audio | [optional] [default to 44100]
**stream** | **bool** | If true, output is streamed for several characters at a time instead of waiting for the full response. The stream terminates with &#x60;data: [DONE]&#x60;. If false, return the encoded audio as octet stream | [optional] [default to False]

## Example

```python
from together.generated.models.audio_speech_request import AudioSpeechRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AudioSpeechRequest from a JSON string
audio_speech_request_instance = AudioSpeechRequest.from_json(json)
# print the JSON string representation of the object
print(AudioSpeechRequest.to_json())

# convert the object into a dict
audio_speech_request_dict = audio_speech_request_instance.to_dict()
# create an instance of AudioSpeechRequest from a dict
audio_speech_request_from_dict = AudioSpeechRequest.from_dict(audio_speech_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
