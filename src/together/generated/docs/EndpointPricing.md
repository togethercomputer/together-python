# EndpointPricing

Pricing details for using an endpoint

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cents_per_minute** | **float** | Cost per minute of endpoint uptime in cents |

## Example

```python
from together.generated.models.endpoint_pricing import EndpointPricing

# TODO update the JSON string below
json = "{}"
# create an instance of EndpointPricing from a JSON string
endpoint_pricing_instance = EndpointPricing.from_json(json)
# print the JSON string representation of the object
print(EndpointPricing.to_json())

# convert the object into a dict
endpoint_pricing_dict = endpoint_pricing_instance.to_dict()
# create an instance of EndpointPricing from a dict
endpoint_pricing_from_dict = EndpointPricing.from_dict(endpoint_pricing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
