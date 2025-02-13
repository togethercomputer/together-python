# CompletionRequestSafetyModel

The name of the moderation model used to validate tokens. Choose from the available moderation models found [here](https://docs.together.ai/docs/inference-models#moderation-models).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.completion_request_safety_model import CompletionRequestSafetyModel

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionRequestSafetyModel from a JSON string
completion_request_safety_model_instance = CompletionRequestSafetyModel.from_json(json)
# print the JSON string representation of the object
print(CompletionRequestSafetyModel.to_json())

# convert the object into a dict
completion_request_safety_model_dict = completion_request_safety_model_instance.to_dict()
# create an instance of CompletionRequestSafetyModel from a dict
completion_request_safety_model_from_dict = CompletionRequestSafetyModel.from_dict(completion_request_safety_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
