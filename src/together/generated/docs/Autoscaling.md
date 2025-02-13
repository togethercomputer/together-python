# Autoscaling

Configuration for automatic scaling of replicas based on demand.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_replicas** | **int** | The minimum number of replicas to maintain, even when there is no load |
**max_replicas** | **int** | The maximum number of replicas to scale up to under load |

## Example

```python
from together.generated.models.autoscaling import Autoscaling

# TODO update the JSON string below
json = "{}"
# create an instance of Autoscaling from a JSON string
autoscaling_instance = Autoscaling.from_json(json)
# print the JSON string representation of the object
print(Autoscaling.to_json())

# convert the object into a dict
autoscaling_dict = autoscaling_instance.to_dict()
# create an instance of Autoscaling from a dict
autoscaling_from_dict = Autoscaling.from_dict(autoscaling_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
