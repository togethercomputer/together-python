# ChatCompletionChoicesDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** |  | [optional]
**index** | **int** |  | [optional]
**seed** | **int** |  | [optional]
**finish_reason** | [**FinishReason**](FinishReason.md) |  | [optional]
**message** | [**ChatCompletionMessage**](ChatCompletionMessage.md) |  | [optional]
**logprobs** | [**ChatCompletionChoicesDataInnerLogprobs**](ChatCompletionChoicesDataInnerLogprobs.md) |  | [optional]

## Example

```python
from together.generated.models.chat_completion_choices_data_inner import ChatCompletionChoicesDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChoicesDataInner from a JSON string
chat_completion_choices_data_inner_instance = ChatCompletionChoicesDataInner.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChoicesDataInner.to_json())

# convert the object into a dict
chat_completion_choices_data_inner_dict = chat_completion_choices_data_inner_instance.to_dict()
# create an instance of ChatCompletionChoicesDataInner from a dict
chat_completion_choices_data_inner_from_dict = ChatCompletionChoicesDataInner.from_dict(chat_completion_choices_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
