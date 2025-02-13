# EmbeddingsResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**embedding** | **List[float]** |  |
**index** | **int** |  |

## Example

```python
from together.generated.models.embeddings_response_data_inner import EmbeddingsResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsResponseDataInner from a JSON string
embeddings_response_data_inner_instance = EmbeddingsResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsResponseDataInner.to_json())

# convert the object into a dict
embeddings_response_data_inner_dict = embeddings_response_data_inner_instance.to_dict()
# create an instance of EmbeddingsResponseDataInner from a dict
embeddings_response_data_inner_from_dict = EmbeddingsResponseDataInner.from_dict(embeddings_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
