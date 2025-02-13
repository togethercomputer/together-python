# FineTunesPostRequestTrainingType


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
from together.generated.models.fine_tunes_post_request_training_type import FineTunesPostRequestTrainingType

# TODO update the JSON string below
json = "{}"
# create an instance of FineTunesPostRequestTrainingType from a JSON string
fine_tunes_post_request_training_type_instance = FineTunesPostRequestTrainingType.from_json(json)
# print the JSON string representation of the object
print(FineTunesPostRequestTrainingType.to_json())

# convert the object into a dict
fine_tunes_post_request_training_type_dict = fine_tunes_post_request_training_type_instance.to_dict()
# create an instance of FineTunesPostRequestTrainingType from a dict
fine_tunes_post_request_training_type_from_dict = FineTunesPostRequestTrainingType.from_dict(fine_tunes_post_request_training_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
