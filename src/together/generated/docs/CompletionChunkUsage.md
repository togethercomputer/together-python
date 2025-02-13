# CompletionChunkUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_tokens** | **int** |  |
**completion_tokens** | **int** |  |
**total_tokens** | **int** |  |

## Example

```python
from together.generated.models.completion_chunk_usage import CompletionChunkUsage

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionChunkUsage from a JSON string
completion_chunk_usage_instance = CompletionChunkUsage.from_json(json)
# print the JSON string representation of the object
print(CompletionChunkUsage.to_json())

# convert the object into a dict
completion_chunk_usage_dict = completion_chunk_usage_instance.to_dict()
# create an instance of CompletionChunkUsage from a dict
completion_chunk_usage_from_dict = CompletionChunkUsage.from_dict(completion_chunk_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
