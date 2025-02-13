# ChatCompletionChoicesDataInnerLogprobs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token_ids** | **List[float]** | List of token IDs corresponding to the logprobs | [optional]
**tokens** | **List[str]** | List of token strings | [optional]
**token_logprobs** | **List[float]** | List of token log probabilities | [optional]

## Example

```python
from together.generated.models.chat_completion_choices_data_inner_logprobs import ChatCompletionChoicesDataInnerLogprobs

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionChoicesDataInnerLogprobs from a JSON string
chat_completion_choices_data_inner_logprobs_instance = ChatCompletionChoicesDataInnerLogprobs.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionChoicesDataInnerLogprobs.to_json())

# convert the object into a dict
chat_completion_choices_data_inner_logprobs_dict = chat_completion_choices_data_inner_logprobs_instance.to_dict()
# create an instance of ChatCompletionChoicesDataInnerLogprobs from a dict
chat_completion_choices_data_inner_logprobs_from_dict = ChatCompletionChoicesDataInnerLogprobs.from_dict(chat_completion_choices_data_inner_logprobs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
