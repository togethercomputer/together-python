# ChatCompletionRequestToolChoice

Controls which (if any) function is called by the model. By default uses `auto`, which lets the model pick between generating a message or calling a function.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** |  |
**id** | **str** |  |
**type** | **str** |  |
**function** | [**ToolChoiceFunction**](ToolChoiceFunction.md) |  |

## Example

```python
from together.generated.models.chat_completion_request_tool_choice import ChatCompletionRequestToolChoice

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestToolChoice from a JSON string
chat_completion_request_tool_choice_instance = ChatCompletionRequestToolChoice.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestToolChoice.to_json())

# convert the object into a dict
chat_completion_request_tool_choice_dict = chat_completion_request_tool_choice_instance.to_dict()
# create an instance of ChatCompletionRequestToolChoice from a dict
chat_completion_request_tool_choice_from_dict = ChatCompletionRequestToolChoice.from_dict(chat_completion_request_tool_choice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
