# ChatCompletionMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  |
**role** | **str** |  |
**name** | **str** |  |
**tool_calls** | [**List[ToolChoice]**](ToolChoice.md) |  | [optional]
**function_call** | [**ChatCompletionMessageFunctionCall**](ChatCompletionMessageFunctionCall.md) |  | [optional]
**tool_call_id** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_message_param import ChatCompletionMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionMessageParam from a JSON string
chat_completion_message_param_instance = ChatCompletionMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionMessageParam.to_json())

# convert the object into a dict
chat_completion_message_param_dict = chat_completion_message_param_instance.to_dict()
# create an instance of ChatCompletionMessageParam from a dict
chat_completion_message_param_from_dict = ChatCompletionMessageParam.from_dict(chat_completion_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
