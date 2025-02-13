# UsageData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_tokens** | **int** |  |
**completion_tokens** | **int** |  |
**total_tokens** | **int** |  |

## Example

```python
from together.generated.models.usage_data import UsageData

# TODO update the JSON string below
json = "{}"
# create an instance of UsageData from a JSON string
usage_data_instance = UsageData.from_json(json)
# print the JSON string representation of the object
print(UsageData.to_json())

# convert the object into a dict
usage_data_dict = usage_data_instance.to_dict()
# create an instance of UsageData from a dict
usage_data_from_dict = UsageData.from_dict(usage_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
