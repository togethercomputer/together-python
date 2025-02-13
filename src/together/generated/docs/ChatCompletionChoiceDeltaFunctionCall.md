# ChatCompletionChoiceDeltaFunctionCall


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**arguments** | **str** |  |
**name** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_choice_delta_function_call import ChatCompletionChoiceDeltaFunctionCall

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChoiceDeltaFunctionCall from a JSON string
chat_completion_choice_delta_function_call_instance = ChatCompletionChoiceDeltaFunctionCall.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChoiceDeltaFunctionCall.to_json())

# convert the object into a dict
chat_completion_choice_delta_function_call_dict = chat_completion_choice_delta_function_call_instance.to_dict()
# create an instance of ChatCompletionChoiceDeltaFunctionCall from a dict
chat_completion_choice_delta_function_call_from_dict = ChatCompletionChoiceDeltaFunctionCall.from_dict(chat_completion_choice_delta_function_call_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
