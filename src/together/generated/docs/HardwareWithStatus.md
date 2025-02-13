# HardwareWithStatus

Hardware configuration details with optional availability status

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**id** | **str** | Unique identifier for the hardware configuration |
**pricing** | [**EndpointPricing**](EndpointPricing.md) |  |
**specs** | [**HardwareSpec**](HardwareSpec.md) |  |
**availability** | [**HardwareAvailability**](HardwareAvailability.md) |  | [optional]
**updated_at** | **datetime** | Timestamp of when the hardware status was last updated |

## Example

```python
from together.generated.models.hardware_with_status import HardwareWithStatus

# TODO update the JSON string below
json = "{}"
# create an instance of HardwareWithStatus from a JSON string
hardware_with_status_instance = HardwareWithStatus.from_json(json)
# print the JSON string representation of the object
print(HardwareWithStatus.to_json())

# convert the object into a dict
hardware_with_status_dict = hardware_with_status_instance.to_dict()
# create an instance of HardwareWithStatus from a dict
hardware_with_status_from_dict = HardwareWithStatus.from_dict(hardware_with_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
