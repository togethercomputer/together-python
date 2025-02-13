# ListHardware200ResponseOneOf1DataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**name** | **str** | Unique identifier for the hardware configuration |
**pricing** | [**EndpointPricing**](EndpointPricing.md) |  |
**specs** | [**HardwareSpec**](HardwareSpec.md) |  |
**availability** | [**HardwareAvailability**](HardwareAvailability.md) |  |
**updated_at** | **datetime** | Timestamp of when the hardware status was last updated |

## Example

```python
from together.generated.models.list_hardware200_response_one_of1_data_inner import ListHardware200ResponseOneOf1DataInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListHardware200ResponseOneOf1DataInner from a JSON string
list_hardware200_response_one_of1_data_inner_instance = ListHardware200ResponseOneOf1DataInner.from_json(json)
# print the JSON string representation of the object
print(ListHardware200ResponseOneOf1DataInner.to_json())

# convert the object into a dict
list_hardware200_response_one_of1_data_inner_dict = list_hardware200_response_one_of1_data_inner_instance.to_dict()
# create an instance of ListHardware200ResponseOneOf1DataInner from a dict
list_hardware200_response_one_of1_data_inner_from_dict = ListHardware200ResponseOneOf1DataInner.from_dict(list_hardware200_response_one_of1_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
