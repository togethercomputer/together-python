# CompletionChoicesDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | [optional]
**seed** | **int** |  | [optional]
**finish_reason** | [**FinishReason**](FinishReason.md) |  | [optional]
**logprobs** | [**LogprobsPart**](.md) |  | [optional]

## Example

```python
from together.generated.models.completion_choices_data_inner import CompletionChoicesDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionChoicesDataInner from a JSON string
completion_choices_data_inner_instance = CompletionChoicesDataInner.from_json(json)
# print the JSON string representation of the object
print(CompletionChoicesDataInner.to_json())

# convert the object into a dict
completion_choices_data_inner_dict = completion_choices_data_inner_instance.to_dict()
# create an instance of CompletionChoicesDataInner from a dict
completion_choices_data_inner_from_dict = CompletionChoicesDataInner.from_dict(completion_choices_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
