# CreateEndpointRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | A human-readable name for the endpoint | [optional]
**model** | **str** | The model to deploy on this endpoint |
**hardware** | **str** | The hardware configuration to use for this endpoint |
**autoscaling** | [**Autoscaling**](Autoscaling.md) | Configuration for automatic scaling of the endpoint |
**disable_prompt_cache** | **bool** | Whether to disable the prompt cache for this endpoint | [optional] [default to False]
**disable_speculative_decoding** | **bool** | Whether to disable speculative decoding for this endpoint | [optional] [default to False]
**state** | **str** | The desired state of the endpoint | [optional] [default to 'STARTED']

## Example

```python
from together.generated.models.create_endpoint_request import CreateEndpointRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEndpointRequest from a JSON string
create_endpoint_request_instance = CreateEndpointRequest.from_json(json)
# print the JSON string representation of the object
print(CreateEndpointRequest.to_json())

# convert the object into a dict
create_endpoint_request_dict = create_endpoint_request_instance.to_dict()
# create an instance of CreateEndpointRequest from a dict
create_endpoint_request_from_dict = CreateEndpointRequest.from_dict(create_endpoint_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
