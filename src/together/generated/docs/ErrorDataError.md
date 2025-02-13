# ErrorDataError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  |
**type** | **str** |  |
**param** | **str** |  | [optional]
**code** | **str** |  | [optional]

## Example

```python
from together.generated.models.error_data_error import ErrorDataError

# TODO update the JSON string below
json = "{}"
# create an instance of ErrorDataError from a JSON string
error_data_error_instance = ErrorDataError.from_json(json)
# print the JSON string representation of the object
print(ErrorDataError.to_json())

# convert the object into a dict
error_data_error_dict = error_data_error_instance.to_dict()
# create an instance of ErrorDataError from a dict
error_data_error_from_dict = ErrorDataError.from_dict(error_data_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
