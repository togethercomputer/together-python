# ListHardware200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**data** | [**List[HardwareWithStatus]**](HardwareWithStatus.md) |  |

## Example

```python
from together.generated.models.list_hardware200_response import ListHardware200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListHardware200Response from a JSON string
list_hardware200_response_instance = ListHardware200Response.from_json(json)
# print the JSON string representation of the object
print(ListHardware200Response.to_json())

# convert the object into a dict
list_hardware200_response_dict = list_hardware200_response_instance.to_dict()
# create an instance of ListHardware200Response from a dict
list_hardware200_response_from_dict = ListHardware200Response.from_dict(list_hardware200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
