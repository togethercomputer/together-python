# HardwareSpec

Detailed specifications of a hardware configuration

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gpu_type** | **str** | The type/model of GPU |
**gpu_link** | **str** | The GPU interconnect technology |
**gpu_memory** | **float** | Amount of GPU memory in GB |
**gpu_count** | **int** | Number of GPUs in this configuration |

## Example

```python
from together.generated.models.hardware_spec import HardwareSpec

# TODO update the JSON string below
json = "{}"
# create an instance of HardwareSpec from a JSON string
hardware_spec_instance = HardwareSpec.from_json(json)
# print the JSON string representation of the object
print(HardwareSpec.to_json())

# convert the object into a dict
hardware_spec_dict = hardware_spec_instance.to_dict()
# create an instance of HardwareSpec from a dict
hardware_spec_from_dict = HardwareSpec.from_dict(hardware_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
