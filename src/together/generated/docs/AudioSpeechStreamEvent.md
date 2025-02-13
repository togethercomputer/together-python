# AudioSpeechStreamEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**AudioSpeechStreamChunk**](AudioSpeechStreamChunk.md) |  |

## Example

```python
from together.generated.models.audio_speech_stream_event import AudioSpeechStreamEvent

# TODO update the JSON string below
json = "{}"
# create an instance of AudioSpeechStreamEvent from a JSON string
audio_speech_stream_event_instance = AudioSpeechStreamEvent.from_json(json)
# print the JSON string representation of the object
print(AudioSpeechStreamEvent.to_json())

# convert the object into a dict
audio_speech_stream_event_dict = audio_speech_stream_event_instance.to_dict()
# create an instance of AudioSpeechStreamEvent from a dict
audio_speech_stream_event_from_dict = AudioSpeechStreamEvent.from_dict(audio_speech_stream_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
