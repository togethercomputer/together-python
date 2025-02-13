# ChatCompletionMessage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  |
**role** | **str** |  |
**tool_calls** | [**List[ToolChoice]**](ToolChoice.md) |  | [optional]
**function_call** | [**ChatCompletionMessageFunctionCall**](ChatCompletionMessageFunctionCall.md) |  | [optional]

## Example

```python
from together.generated.models.chat_completion_message import ChatCompletionMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionMessage from a JSON string
chat_completion_message_instance = ChatCompletionMessage.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionMessage.to_json())

# convert the object into a dict
chat_completion_message_dict = chat_completion_message_instance.to_dict()
# create an instance of ChatCompletionMessage from a dict
chat_completion_message_from_dict = ChatCompletionMessage.from_dict(chat_completion_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
