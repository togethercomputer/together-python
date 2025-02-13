# EmbeddingsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**model** | **str** |  |
**data** | [**List[EmbeddingsResponseDataInner]**](EmbeddingsResponseDataInner.md) |  |

## Example

```python
from together.generated.models.embeddings_response import EmbeddingsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsResponse from a JSON string
embeddings_response_instance = EmbeddingsResponse.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsResponse.to_json())

# convert the object into a dict
embeddings_response_dict = embeddings_response_instance.to_dict()
# create an instance of EmbeddingsResponse from a dict
embeddings_response_from_dict = EmbeddingsResponse.from_dict(embeddings_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
