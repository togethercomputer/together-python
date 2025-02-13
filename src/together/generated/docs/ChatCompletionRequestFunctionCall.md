# ChatCompletionRequestFunctionCall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_request_function_call import ChatCompletionRequestFunctionCall

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestFunctionCall from a JSON string
chat_completion_request_function_call_instance = ChatCompletionRequestFunctionCall.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestFunctionCall.to_json())

# convert the object into a dict
chat_completion_request_function_call_dict = chat_completion_request_function_call_instance.to_dict()
# create an instance of ChatCompletionRequestFunctionCall from a dict
chat_completion_request_function_call_from_dict = ChatCompletionRequestFunctionCall.from_dict(chat_completion_request_function_call_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
