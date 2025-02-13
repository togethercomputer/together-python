# ToolsPartFunction


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional]
**name** | **str** |  | [optional]
**parameters** | **Dict[str, object]** | A map of parameter names to their values. | [optional]

## Example

```python
from together.generated.models.tools_part_function import ToolsPartFunction

# TODO update the JSON string below
json = "{}"
# create an instance of ToolsPartFunction from a JSON string
tools_part_function_instance = ToolsPartFunction.from_json(json)
# print the JSON string representation of the object
print(ToolsPartFunction.to_json())

# convert the object into a dict
tools_part_function_dict = tools_part_function_instance.to_dict()
# create an instance of ToolsPartFunction from a dict
tools_part_function_from_dict = ToolsPartFunction.from_dict(tools_part_function_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
