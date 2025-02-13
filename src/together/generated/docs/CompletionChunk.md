# CompletionChunk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  |
**token** | [**CompletionToken**](CompletionToken.md) |  |
**choices** | [**List[CompletionChoice]**](CompletionChoice.md) |  |
**usage** | [**CompletionChunkUsage**](CompletionChunkUsage.md) |  |
**seed** | **int** |  | [optional]
**finish_reason** | [**FinishReason**](FinishReason.md) |  |

## Example

```python
from together.generated.models.completion_chunk import CompletionChunk

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionChunk from a JSON string
completion_chunk_instance = CompletionChunk.from_json(json)
# print the JSON string representation of the object
print(CompletionChunk.to_json())

# convert the object into a dict
completion_chunk_dict = completion_chunk_instance.to_dict()
# create an instance of CompletionChunk from a dict
completion_chunk_from_dict = CompletionChunk.from_dict(completion_chunk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
