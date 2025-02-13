# EmbeddingsRequestModel

The name of the embedding model to use.<br> <br> [See all of Together AI's embedding models](https://docs.together.ai/docs/serverless-models#embedding-models)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.embeddings_request_model import EmbeddingsRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of EmbeddingsRequestModel from a JSON string
embeddings_request_model_instance = EmbeddingsRequestModel.from_json(json)
# print the JSON string representation of the object
print(EmbeddingsRequestModel.to_json())

# convert the object into a dict
embeddings_request_model_dict = embeddings_request_model_instance.to_dict()
# create an instance of EmbeddingsRequestModel from a dict
embeddings_request_model_from_dict = EmbeddingsRequestModel.from_dict(embeddings_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
