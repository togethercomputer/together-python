# ToolsPart


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional]
**function** | [**ToolsPartFunction**](ToolsPartFunction.md) |  | [optional]

## Example

```python
from together.generated.models.tools_part import ToolsPart

# TODO update the JSON string below
json = "{}"
# create an instance of ToolsPart from a JSON string
tools_part_instance = ToolsPart.from_json(json)
# print the JSON string representation of the object
print(ToolsPart.to_json())

# convert the object into a dict
tools_part_dict = tools_part_instance.to_dict()
# create an instance of ToolsPart from a dict
tools_part_from_dict = ToolsPart.from_dict(tools_part_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
