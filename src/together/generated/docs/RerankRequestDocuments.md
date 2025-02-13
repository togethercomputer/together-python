# RerankRequestDocuments

List of documents, which can be either strings or objects.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.rerank_request_documents import RerankRequestDocuments

# TODO update the JSON string below
json = "{}"
# create an instance of RerankRequestDocuments from a JSON string
rerank_request_documents_instance = RerankRequestDocuments.from_json(json)
# print the JSON string representation of the object
print(RerankRequestDocuments.to_json())

# convert the object into a dict
rerank_request_documents_dict = rerank_request_documents_instance.to_dict()
# create an instance of RerankRequestDocuments from a dict
rerank_request_documents_from_dict = RerankRequestDocuments.from_dict(rerank_request_documents_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
