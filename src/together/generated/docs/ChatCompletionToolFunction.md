# ChatCompletionToolFunction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional]
**name** | **str** |  |
**parameters** | **Dict[str, object]** |  | [optional]

## Example

```python
from together.generated.models.chat_completion_tool_function import ChatCompletionToolFunction

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionToolFunction from a JSON string
chat_completion_tool_function_instance = ChatCompletionToolFunction.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionToolFunction.to_json())

# convert the object into a dict
chat_completion_tool_function_dict = chat_completion_tool_function_instance.to_dict()
# create an instance of ChatCompletionToolFunction from a dict
chat_completion_tool_function_from_dict = ChatCompletionToolFunction.from_dict(chat_completion_tool_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
