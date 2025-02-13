# ChatCompletionChoice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int** |  |
**finish_reason** | [**FinishReason**](FinishReason.md) |  |
**logprobs** | [**LogprobsPart**](LogprobsPart.md) |  | [optional]
**delta** | [**ChatCompletionChoiceDelta**](ChatCompletionChoiceDelta.md) |  |

## Example

```python
from together.generated.models.chat_completion_choice import ChatCompletionChoice

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChoice from a JSON string
chat_completion_choice_instance = ChatCompletionChoice.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChoice.to_json())

# convert the object into a dict
chat_completion_choice_dict = chat_completion_choice_instance.to_dict()
# create an instance of ChatCompletionChoice from a dict
chat_completion_choice_from_dict = ChatCompletionChoice.from_dict(chat_completion_choice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
