# RerankRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model** | [**RerankRequestModel**](RerankRequestModel.md) |  |
**query** | **str** | The search query to be used for ranking. |
**documents** | [**RerankRequestDocuments**](RerankRequestDocuments.md) |  |
**top_n** | **int** | The number of top results to return. | [optional]
**return_documents** | **bool** | Whether to return supplied documents with the response. | [optional]
**rank_fields** | **List[str]** | List of keys in the JSON Object document to rank by. Defaults to use all supplied keys for ranking. | [optional]

## Example

```python
from together.generated.models.rerank_request import RerankRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RerankRequest from a JSON string
rerank_request_instance = RerankRequest.from_json(json)
# print the JSON string representation of the object
print(RerankRequest.to_json())

# convert the object into a dict
rerank_request_dict = rerank_request_instance.to_dict()
# create an instance of RerankRequest from a dict
rerank_request_from_dict = RerankRequest.from_dict(rerank_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
