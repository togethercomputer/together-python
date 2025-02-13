# ChatCompletionSystemMessageParam


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **str** |  |
**role** | **str** |  |
**name** | **str** |  | [optional]

## Example

```python
from together.generated.models.chat_completion_system_message_param import ChatCompletionSystemMessageParam

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionSystemMessageParam from a JSON string
chat_completion_system_message_param_instance = ChatCompletionSystemMessageParam.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionSystemMessageParam.to_json())

# convert the object into a dict
chat_completion_system_message_param_dict = chat_completion_system_message_param_instance.to_dict()
# create an instance of ChatCompletionSystemMessageParam from a dict
chat_completion_system_message_param_from_dict = ChatCompletionSystemMessageParam.from_dict(chat_completion_system_message_param_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
