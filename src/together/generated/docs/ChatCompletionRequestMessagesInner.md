# ChatCompletionRequestMessagesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role** | **str** | The role of the messages author. Choice between: system, user, or assistant. |
**content** | **str** | The content of the message, which can either be a simple string or a structured format. |

## Example

```python
from together.generated.models.chat_completion_request_messages_inner import ChatCompletionRequestMessagesInner

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionRequestMessagesInner from a JSON string
chat_completion_request_messages_inner_instance = ChatCompletionRequestMessagesInner.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionRequestMessagesInner.to_json())

# convert the object into a dict
chat_completion_request_messages_inner_dict = chat_completion_request_messages_inner_instance.to_dict()
# create an instance of ChatCompletionRequestMessagesInner from a dict
chat_completion_request_messages_inner_from_dict = ChatCompletionRequestMessagesInner.from_dict(chat_completion_request_messages_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
