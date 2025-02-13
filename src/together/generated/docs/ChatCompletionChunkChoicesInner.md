# ChatCompletionChunkChoicesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int** |  |
**finish_reason** | [**FinishReason**](FinishReason.md) |  |
**logprobs** | **float** |  | [optional]
**seed** | **int** |  | [optional]
**delta** | [**ChatCompletionChoiceDelta**](ChatCompletionChoiceDelta.md) |  |

## Example

```python
from together.generated.models.chat_completion_chunk_choices_inner import ChatCompletionChunkChoicesInner

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChunkChoicesInner from a JSON string
chat_completion_chunk_choices_inner_instance = ChatCompletionChunkChoicesInner.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChunkChoicesInner.to_json())

# convert the object into a dict
chat_completion_chunk_choices_inner_dict = chat_completion_chunk_choices_inner_instance.to_dict()
# create an instance of ChatCompletionChunkChoicesInner from a dict
chat_completion_chunk_choices_inner_from_dict = ChatCompletionChunkChoicesInner.from_dict(chat_completion_chunk_choices_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
