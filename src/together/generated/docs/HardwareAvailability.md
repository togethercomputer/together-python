# HardwareAvailability

Indicates the current availability status of a hardware configuration

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The availability status of the hardware configuration |

## Example

```python
from together.generated.models.hardware_availability import HardwareAvailability

# TODO update the JSON string below
json = "{}"
# create an instance of HardwareAvailability from a JSON string
hardware_availability_instance = HardwareAvailability.from_json(json)
# print the JSON string representation of the object
print(HardwareAvailability.to_json())

# convert the object into a dict
hardware_availability_dict = hardware_availability_instance.to_dict()
# create an instance of HardwareAvailability from a dict
hardware_availability_from_dict = HardwareAvailability.from_dict(hardware_availability_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
