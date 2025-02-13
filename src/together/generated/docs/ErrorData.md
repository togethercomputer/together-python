# ErrorData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**ErrorDataError**](ErrorDataError.md) |  |

## Example

```python
from together.generated.models.error_data import ErrorData

# TODO update the JSON string below
json = "{}"
# create an instance of ErrorData from a JSON string
error_data_instance = ErrorData.from_json(json)
# print the JSON string representation of the object
print(ErrorData.to_json())

# convert the object into a dict
error_data_dict = error_data_instance.to_dict()
# create an instance of ErrorData from a dict
error_data_from_dict = ErrorData.from_dict(error_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
