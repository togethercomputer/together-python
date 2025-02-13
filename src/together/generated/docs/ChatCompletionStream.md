# ChatCompletionStream


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_stream import ChatCompletionStream

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionStream from a JSON string
chat_completion_stream_instance = ChatCompletionStream.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionStream.to_json())

# convert the object into a dict
chat_completion_stream_dict = chat_completion_stream_instance.to_dict()
# create an instance of ChatCompletionStream from a dict
chat_completion_stream_from_dict = ChatCompletionStream.from_dict(chat_completion_stream_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
