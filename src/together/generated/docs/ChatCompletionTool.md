# ChatCompletionTool


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  |
**function** | [**ChatCompletionToolFunction**](ChatCompletionToolFunction.md) |  |

## Example

```python
from together.generated.models.chat_completion_tool import ChatCompletionTool

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionTool from a JSON string
chat_completion_tool_instance = ChatCompletionTool.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionTool.to_json())

# convert the object into a dict
chat_completion_tool_dict = chat_completion_tool_instance.to_dict()
# create an instance of ChatCompletionTool from a dict
chat_completion_tool_from_dict = ChatCompletionTool.from_dict(chat_completion_tool_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
