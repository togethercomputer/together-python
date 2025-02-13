# ChatCompletionFunctionMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role** | **str** |  |
**content** | **str** |  |
**name** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_function_message_param import ChatCompletionFunctionMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionFunctionMessageParam from a JSON string
chat_completion_function_message_param_instance = ChatCompletionFunctionMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionFunctionMessageParam.to_json())

# convert the object into a dict
chat_completion_function_message_param_dict = chat_completion_function_message_param_instance.to_dict()
# create an instance of ChatCompletionFunctionMessageParam from a dict
chat_completion_function_message_param_from_dict = ChatCompletionFunctionMessageParam.from_dict(chat_completion_function_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
