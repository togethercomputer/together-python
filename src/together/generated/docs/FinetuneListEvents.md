# FinetuneListEvents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[FineTuneEvent]**](FineTuneEvent.md) |  |

## Example

```python
from together.generated.models.finetune_list_events import FinetuneListEvents

# TODO update the JSON string below
json = "{}"
# create an instance of FinetuneListEvents from a JSON string
finetune_list_events_instance = FinetuneListEvents.from_json(json)
# print the JSON string representation of the object
print(FinetuneListEvents.to_json())

# convert the object into a dict
finetune_list_events_dict = finetune_list_events_instance.to_dict()
# create an instance of FinetuneListEvents from a dict
finetune_list_events_from_dict = FinetuneListEvents.from_dict(finetune_list_events_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
