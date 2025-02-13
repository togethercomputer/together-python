# ChatCompletionEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ChatCompletionChunk**](ChatCompletionChunk.md) |  |

## Example

```python
from together.generated.models.chat_completion_event import ChatCompletionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionEvent from a JSON string
chat_completion_event_instance = ChatCompletionEvent.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionEvent.to_json())

# convert the object into a dict
chat_completion_event_dict = chat_completion_event_instance.to_dict()
# create an instance of ChatCompletionEvent from a dict
chat_completion_event_from_dict = ChatCompletionEvent.from_dict(chat_completion_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
