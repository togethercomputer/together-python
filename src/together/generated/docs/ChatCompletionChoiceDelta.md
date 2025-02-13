# ChatCompletionChoiceDelta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token_id** | **int** |  | [optional]
**role** | **str** |  |
**content** | **str** |  | [optional]
**tool_calls** | [**List[ToolChoice]**](ToolChoice.md) |  | [optional]
**function_call** | [**ChatCompletionChoiceDeltaFunctionCall**](ChatCompletionChoiceDeltaFunctionCall.md) |  | [optional]

## Example

```python
from together.generated.models.chat_completion_choice_delta import ChatCompletionChoiceDelta

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChoiceDelta from a JSON string
chat_completion_choice_delta_instance = ChatCompletionChoiceDelta.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChoiceDelta.to_json())

# convert the object into a dict
chat_completion_choice_delta_dict = chat_completion_choice_delta_instance.to_dict()
# create an instance of ChatCompletionChoiceDelta from a dict
chat_completion_choice_delta_from_dict = ChatCompletionChoiceDelta.from_dict(chat_completion_choice_delta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
