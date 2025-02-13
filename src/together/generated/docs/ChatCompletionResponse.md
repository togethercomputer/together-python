# ChatCompletionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  |
**choices** | [**List[ChatCompletionChoicesDataInner]**](ChatCompletionChoicesDataInner.md) |  |
**usage** | [**UsageData**](UsageData.md) |  | [optional]
**created** | **int** |  |
**model** | **str** |  |
**object** | **str** |  |

## Example

```python
from together.generated.models.chat_completion_response import ChatCompletionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionResponse from a JSON string
chat_completion_response_instance = ChatCompletionResponse.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionResponse.to_json())

# convert the object into a dict
chat_completion_response_dict = chat_completion_response_instance.to_dict()
# create an instance of ChatCompletionResponse from a dict
chat_completion_response_from_dict = ChatCompletionResponse.from_dict(chat_completion_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
