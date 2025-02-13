# LRScheduler


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lr_scheduler_type** | **str** |  |
**lr_scheduler_args** | [**LinearLRSchedulerArgs**](.md) |  | [optional]

## Example

```python
from together.generated.models.lr_scheduler import LRScheduler

# TODO update the JSON string below
json = "{}"
# create an instance of LRScheduler from a JSON string
lr_scheduler_instance = LRScheduler.from_json(json)
# print the JSON string representation of the object
print(LRScheduler.to_json())

# convert the object into a dict
lr_scheduler_dict = lr_scheduler_instance.to_dict()
# create an instance of LRScheduler from a dict
lr_scheduler_from_dict = LRScheduler.from_dict(lr_scheduler_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
