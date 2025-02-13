# ListEndpoint

Details about an endpoint when listed via the list endpoint

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** | The type of object |
**id** | **str** | Unique identifier for the endpoint |
**name** | **str** | System name for the endpoint |
**model** | **str** | The model deployed on this endpoint |
**type** | **str** | The type of endpoint |
**owner** | **str** | The owner of this endpoint |
**state** | **str** | Current state of the endpoint |
**created_at** | **datetime** | Timestamp when the endpoint was created |

## Example

```python
from together.generated.models.list_endpoint import ListEndpoint

# TODO update the JSON string below
json = "{}"
# create an instance of ListEndpoint from a JSON string
list_endpoint_instance = ListEndpoint.from_json(json)
# print the JSON string representation of the object
print(ListEndpoint.to_json())

# convert the object into a dict
list_endpoint_dict = list_endpoint_instance.to_dict()
# create an instance of ListEndpoint from a dict
list_endpoint_from_dict = ListEndpoint.from_dict(list_endpoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
