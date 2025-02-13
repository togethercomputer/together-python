# ChatCompletionAssistantMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  | [optional]
**role** | **str** |  |
**name** | **str** |  | [optional]
**tool_calls** | [**List[ToolChoice]**](ToolChoice.md) |  | [optional]
**function_call** | [**ChatCompletionMessageFunctionCall**](ChatCompletionMessageFunctionCall.md) |  | [optional]

## Example

```python
from together.generated.models.chat_completion_assistant_message_param import ChatCompletionAssistantMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionAssistantMessageParam from a JSON string
chat_completion_assistant_message_param_instance = ChatCompletionAssistantMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionAssistantMessageParam.to_json())

# convert the object into a dict
chat_completion_assistant_message_param_dict = chat_completion_assistant_message_param_instance.to_dict()
# create an instance of ChatCompletionAssistantMessageParam from a dict
chat_completion_assistant_message_param_from_dict = ChatCompletionAssistantMessageParam.from_dict(chat_completion_assistant_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
