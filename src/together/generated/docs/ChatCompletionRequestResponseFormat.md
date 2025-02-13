# ChatCompletionRequestResponseFormat

An object specifying the format that the model must output.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of the response format. | [optional]
**var_schema** | **Dict[str, str]** | The schema of the response format. | [optional]

## Example

```python
from together.generated.models.chat_completion_request_response_format import ChatCompletionRequestResponseFormat

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestResponseFormat from a JSON string
chat_completion_request_response_format_instance = ChatCompletionRequestResponseFormat.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestResponseFormat.to_json())

# convert the object into a dict
chat_completion_request_response_format_dict = chat_completion_request_response_format_instance.to_dict()
# create an instance of ChatCompletionRequestResponseFormat from a dict
chat_completion_request_response_format_from_dict = ChatCompletionRequestResponseFormat.from_dict(chat_completion_request_response_format_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
