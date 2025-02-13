# FinetuneList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[FinetuneResponse]**](FinetuneResponse.md) |  |

## Example

```python
from together.generated.models.finetune_list import FinetuneList

# TODO update the JSON string below
json = "{}"
# create an instance of FinetuneList from a JSON string
finetune_list_instance = FinetuneList.from_json(json)
# print the JSON string representation of the object
print(FinetuneList.to_json())

# convert the object into a dict
finetune_list_dict = finetune_list_instance.to_dict()
# create an instance of FinetuneList from a dict
finetune_list_from_dict = FinetuneList.from_dict(finetune_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
