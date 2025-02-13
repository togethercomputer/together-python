# ToolChoice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **float** |  |
**id** | **str** |  |
**type** | **str** |  |
**function** | [**ToolChoiceFunction**](ToolChoiceFunction.md) |  |

## Example

```python
from together.generated.models.tool_choice import ToolChoice

# TODO update the JSON string below
json = "{}"
# create an instance of ToolChoice from a JSON string
tool_choice_instance = ToolChoice.from_json(json)
# print the JSON string representation of the object
print(ToolChoice.to_json())

# convert the object into a dict
tool_choice_dict = tool_choice_instance.to_dict()
# create an instance of ToolChoice from a dict
tool_choice_from_dict = ToolChoice.from_dict(tool_choice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
