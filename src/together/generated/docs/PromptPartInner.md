# PromptPartInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | [optional]
**logprobs** | [**LogprobsPart**](LogprobsPart.md) |  | [optional]

## Example

```python
from together.generated.models.prompt_part_inner import PromptPartInner

# TODO update the JSON string below
json = "{}"
# create an instance of PromptPartInner from a JSON string
prompt_part_inner_instance = PromptPartInner.from_json(json)
# print the JSON string representation of the object
print(PromptPartInner.to_json())

# convert the object into a dict
prompt_part_inner_dict = prompt_part_inner_instance.to_dict()
# create an instance of PromptPartInner from a dict
prompt_part_inner_from_dict = PromptPartInner.from_dict(prompt_part_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
