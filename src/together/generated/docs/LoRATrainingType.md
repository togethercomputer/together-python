# LoRATrainingType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  |
**lora_r** | **int** |  |
**lora_alpha** | **int** |  |
**lora_dropout** | **float** |  | [optional] [default to 0.0]
**lora_trainable_modules** | **str** |  | [optional] [default to 'all-linear']

## Example

```python
from together.generated.models.lo_ra_training_type import LoRATrainingType

# TODO update the JSON string below
json = "{}"
# create an instance of LoRATrainingType from a JSON string
lo_ra_training_type_instance = LoRATrainingType.from_json(json)
# print the JSON string representation of the object
print(LoRATrainingType.to_json())

# convert the object into a dict
lo_ra_training_type_dict = lo_ra_training_type_instance.to_dict()
# create an instance of LoRATrainingType from a dict
lo_ra_training_type_from_dict = LoRATrainingType.from_dict(lo_ra_training_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
