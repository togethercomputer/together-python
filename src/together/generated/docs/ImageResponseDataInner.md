# ImageResponseDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int** |  |
**b64_json** | **str** |  | [optional]
**url** | **str** |  | [optional]

## Example

```python
from together.generated.models.image_response_data_inner import ImageResponseDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of ImageResponseDataInner from a JSON string
image_response_data_inner_instance = ImageResponseDataInner.from_json(json)
# print the JSON string representation of the object
print(ImageResponseDataInner.to_json())

# convert the object into a dict
image_response_data_inner_dict = image_response_data_inner_instance.to_dict()
# create an instance of ImageResponseDataInner from a dict
image_response_data_inner_from_dict = ImageResponseDataInner.from_dict(image_response_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
