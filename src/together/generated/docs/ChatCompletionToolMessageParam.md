# ChatCompletionToolMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role** | **str** |  |
**content** | **str** |  |
**tool_call_id** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_tool_message_param import ChatCompletionToolMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionToolMessageParam from a JSON string
chat_completion_tool_message_param_instance = ChatCompletionToolMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionToolMessageParam.to_json())

# convert the object into a dict
chat_completion_tool_message_param_dict = chat_completion_tool_message_param_instance.to_dict()
# create an instance of ChatCompletionToolMessageParam from a dict
chat_completion_tool_message_param_from_dict = ChatCompletionToolMessageParam.from_dict(chat_completion_tool_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
