# RerankResponseResultsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int** |  |
**relevance_score** | **float** |  |
**document** | [**RerankResponseResultsInnerDocument**](RerankResponseResultsInnerDocument.md) |  |

## Example

```python
from together.generated.models.rerank_response_results_inner import RerankResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of RerankResponseResultsInner from a JSON string
rerank_response_results_inner_instance = RerankResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(RerankResponseResultsInner.to_json())

# convert the object into a dict
rerank_response_results_inner_dict = rerank_response_results_inner_instance.to_dict()
# create an instance of RerankResponseResultsInner from a dict
rerank_response_results_inner_from_dict = RerankResponseResultsInner.from_dict(rerank_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
