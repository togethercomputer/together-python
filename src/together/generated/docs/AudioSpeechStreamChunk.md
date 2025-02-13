# AudioSpeechStreamChunk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**model** | **str** |  |
**b64** | **str** | base64 encoded audio stream |

## Example

```python
from together.generated.models.audio_speech_stream_chunk import AudioSpeechStreamChunk

# TODO update the JSON string below
json = "{}"
# create an instance of AudioSpeechStreamChunk from a JSON string
audio_speech_stream_chunk_instance = AudioSpeechStreamChunk.from_json(json)
# print the JSON string representation of the object
print(AudioSpeechStreamChunk.to_json())

# convert the object into a dict
audio_speech_stream_chunk_dict = audio_speech_stream_chunk_instance.to_dict()
# create an instance of AudioSpeechStreamChunk from a dict
audio_speech_stream_chunk_from_dict = AudioSpeechStreamChunk.from_dict(audio_speech_stream_chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
