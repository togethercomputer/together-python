# ListHardware200ResponseOneOf

Response when no model filter is provided

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**data** | [**List[ListHardware200ResponseOneOfDataInner]**](ListHardware200ResponseOneOfDataInner.md) |  |

## Example

```python
from together.generated.models.list_hardware200_response_one_of import ListHardware200ResponseOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of ListHardware200ResponseOneOf from a JSON string
list_hardware200_response_one_of_instance = ListHardware200ResponseOneOf.from_json(json)
# print the JSON string representation of the object
print(ListHardware200ResponseOneOf.to_json())

# convert the object into a dict
list_hardware200_response_one_of_dict = list_hardware200_response_one_of_instance.to_dict()
# create an instance of ListHardware200ResponseOneOf from a dict
list_hardware200_response_one_of_from_dict = ListHardware200ResponseOneOf.from_dict(list_hardware200_response_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
