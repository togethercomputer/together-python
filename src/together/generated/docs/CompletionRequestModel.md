# CompletionRequestModel

The name of the model to query.<br> <br> [See all of Together AI's chat models](https://docs.together.ai/docs/serverless-models#chat-models)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.completion_request_model import CompletionRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionRequestModel from a JSON string
completion_request_model_instance = CompletionRequestModel.from_json(json)
# print the JSON string representation of the object
print(CompletionRequestModel.to_json())

# convert the object into a dict
completion_request_model_dict = completion_request_model_instance.to_dict()
# create an instance of CompletionRequestModel from a dict
completion_request_model_from_dict = CompletionRequestModel.from_dict(completion_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
