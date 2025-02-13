# ModelInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  |
**object** | **str** |  |
**created** | **int** |  |
**type** | **str** |  |
**display_name** | **str** |  | [optional]
**organization** | **str** |  | [optional]
**link** | **str** |  | [optional]
**license** | **str** |  | [optional]
**context_length** | **int** |  | [optional]
**pricing** | [**Pricing**](Pricing.md) |  | [optional]

## Example

```python
from together.generated.models.model_info import ModelInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ModelInfo from a JSON string
model_info_instance = ModelInfo.from_json(json)
# print the JSON string representation of the object
print(ModelInfo.to_json())

# convert the object into a dict
model_info_dict = model_info_instance.to_dict()
# create an instance of ModelInfo from a dict
model_info_from_dict = ModelInfo.from_dict(model_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
