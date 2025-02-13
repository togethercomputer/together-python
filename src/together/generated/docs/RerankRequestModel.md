# RerankRequestModel

The model to be used for the rerank request.<br> <br> [See all of Together AI's rerank models](https://docs.together.ai/docs/serverless-models#rerank-models)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.rerank_request_model import RerankRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of RerankRequestModel from a JSON string
rerank_request_model_instance = RerankRequestModel.from_json(json)
# print the JSON string representation of the object
print(RerankRequestModel.to_json())

# convert the object into a dict
rerank_request_model_dict = rerank_request_model_instance.to_dict()
# create an instance of RerankRequestModel from a dict
rerank_request_model_from_dict = RerankRequestModel.from_dict(rerank_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
