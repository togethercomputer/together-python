# LinearLRSchedulerArgs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_lr_ratio** | **float** | The ratio of the final learning rate to the peak learning rate | [optional] [default to 0.0]

## Example

```python
from together.generated.models.linear_lr_scheduler_args import LinearLRSchedulerArgs

# TODO update the JSON string below
json = "{}"
# create an instance of LinearLRSchedulerArgs from a JSON string
linear_lr_scheduler_args_instance = LinearLRSchedulerArgs.from_json(json)
# print the JSON string representation of the object
print(LinearLRSchedulerArgs.to_json())

# convert the object into a dict
linear_lr_scheduler_args_dict = linear_lr_scheduler_args_instance.to_dict()
# create an instance of LinearLRSchedulerArgs from a dict
linear_lr_scheduler_args_from_dict = LinearLRSchedulerArgs.from_dict(linear_lr_scheduler_args_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
