# DedicatedEndpoint

Details about a dedicated endpoint deployment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** | The type of object |
**id** | **str** | Unique identifier for the endpoint |
**name** | **str** | System name for the endpoint |
**display_name** | **str** | Human-readable name for the endpoint |
**model** | **str** | The model deployed on this endpoint |
**hardware** | **str** | The hardware configuration used for this endpoint |
**type** | **str** | The type of endpoint |
**owner** | **str** | The owner of this endpoint |
**state** | **str** | Current state of the endpoint |
**autoscaling** | [**Autoscaling**](Autoscaling.md) | Configuration for automatic scaling of the endpoint |
**created_at** | **datetime** | Timestamp when the endpoint was created |

## Example

```python
from together.generated.models.dedicated_endpoint import DedicatedEndpoint

# TODO update the JSON string below
json = "{}"
# create an instance of DedicatedEndpoint from a JSON string
dedicated_endpoint_instance = DedicatedEndpoint.from_json(json)
# print the JSON string representation of the object
print(DedicatedEndpoint.to_json())

# convert the object into a dict
dedicated_endpoint_dict = dedicated_endpoint_instance.to_dict()
# create an instance of DedicatedEndpoint from a dict
dedicated_endpoint_from_dict = DedicatedEndpoint.from_dict(dedicated_endpoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
