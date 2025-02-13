# EmbeddingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | [**EmbeddingsRequestModel**](EmbeddingsRequestModel.md) |  |
**input** | [**EmbeddingsRequestInput**](EmbeddingsRequestInput.md) |  |

## Example

```python
from together.generated.models.embeddings_request import EmbeddingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsRequest from a JSON string
embeddings_request_instance = EmbeddingsRequest.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsRequest.to_json())

# convert the object into a dict
embeddings_request_dict = embeddings_request_instance.to_dict()
# create an instance of EmbeddingsRequest from a dict
embeddings_request_from_dict = EmbeddingsRequest.from_dict(embeddings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
