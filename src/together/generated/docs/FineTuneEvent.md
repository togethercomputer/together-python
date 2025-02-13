# FineTuneEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  |
**created_at** | **str** |  |
**level** | [**FinetuneEventLevels**](FinetuneEventLevels.md) |  | [optional]
**message** | **str** |  |
**type** | [**FinetuneEventType**](FinetuneEventType.md) |  |
**param_count** | **int** |  |
**token_count** | **int** |  |
**total_steps** | **int** |  |
**wandb_url** | **str** |  |
**step** | **int** |  |
**checkpoint_path** | **str** |  |
**model_path** | **str** |  |
**training_offset** | **int** |  |
**hash** | **str** |  |

## Example

```python
from together.generated.models.fine_tune_event import FineTuneEvent

# TODO update the JSON string below
json = "{}"
# create an instance of FineTuneEvent from a JSON string
fine_tune_event_instance = FineTuneEvent.from_json(json)
# print the JSON string representation of the object
print(FineTuneEvent.to_json())

# convert the object into a dict
fine_tune_event_dict = fine_tune_event_instance.to_dict()
# create an instance of FineTuneEvent from a dict
fine_tune_event_from_dict = FineTuneEvent.from_dict(fine_tune_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
