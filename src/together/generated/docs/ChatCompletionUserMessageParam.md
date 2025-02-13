# ChatCompletionUserMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  |
**role** | **str** |  |
**name** | **str** |  | [optional]

## Example

```python
from together.generated.models.chat_completion_user_message_param import ChatCompletionUserMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionUserMessageParam from a JSON string
chat_completion_user_message_param_instance = ChatCompletionUserMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionUserMessageParam.to_json())

# convert the object into a dict
chat_completion_user_message_param_dict = chat_completion_user_message_param_instance.to_dict()
# create an instance of ChatCompletionUserMessageParam from a dict
chat_completion_user_message_param_from_dict = ChatCompletionUserMessageParam.from_dict(chat_completion_user_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
