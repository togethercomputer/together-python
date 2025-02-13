# ListHardware200ResponseOneOfDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**name** | **str** | Unique identifier for the hardware configuration |
**pricing** | [**EndpointPricing**](EndpointPricing.md) |  |
**specs** | [**HardwareSpec**](HardwareSpec.md) |  |
**availability** | **object** |  | [optional]
**updated_at** | **datetime** | Timestamp of when the hardware status was last updated |

## Example

```python
from together.generated.models.list_hardware200_response_one_of_data_inner import ListHardware200ResponseOneOfDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListHardware200ResponseOneOfDataInner from a JSON string
list_hardware200_response_one_of_data_inner_instance = ListHardware200ResponseOneOfDataInner.from_json(json)
# print the JSON string representation of the object
print(ListHardware200ResponseOneOfDataInner.to_json())

# convert the object into a dict
list_hardware200_response_one_of_data_inner_dict = list_hardware200_response_one_of_data_inner_instance.to_dict()
# create an instance of ListHardware200ResponseOneOfDataInner from a dict
list_hardware200_response_one_of_data_inner_from_dict = ListHardware200ResponseOneOfDataInner.from_dict(list_hardware200_response_one_of_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
