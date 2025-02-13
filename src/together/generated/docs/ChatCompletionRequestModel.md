# ChatCompletionRequestModel

The name of the model to query.<br> <br> [See all of Together AI's chat models](https://docs.together.ai/docs/serverless-models#chat-models)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.chat_completion_request_model import ChatCompletionRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestModel from a JSON string
chat_completion_request_model_instance = ChatCompletionRequestModel.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestModel.to_json())

# convert the object into a dict
chat_completion_request_model_dict = chat_completion_request_model_instance.to_dict()
# create an instance of ChatCompletionRequestModel from a dict
chat_completion_request_model_from_dict = ChatCompletionRequestModel.from_dict(chat_completion_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
