# UpdateEndpointRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | A human-readable name for the endpoint | [optional]
**state** | **str** | The desired state of the endpoint | [optional]
**autoscaling** | [**Autoscaling**](Autoscaling.md) | New autoscaling configuration for the endpoint | [optional]

## Example

```python
from together.generated.models.update_endpoint_request import UpdateEndpointRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEndpointRequest from a JSON string
update_endpoint_request_instance = UpdateEndpointRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateEndpointRequest.to_json())

# convert the object into a dict
update_endpoint_request_dict = update_endpoint_request_instance.to_dict()
# create an instance of UpdateEndpointRequest from a dict
update_endpoint_request_from_dict = UpdateEndpointRequest.from_dict(update_endpoint_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
