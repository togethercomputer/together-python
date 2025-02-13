# ChatCompletionToken


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  |
**text** | **str** |  |
**logprob** | **float** |  |
**special** | **bool** |  |

## Example

```python
from together.generated.models.chat_completion_token import ChatCompletionToken

# TODO update the JSON string below
json = "{}"
# create an instance of ChatCompletionToken from a JSON string
chat_completion_token_instance = ChatCompletionToken.from_json(json)
# print the JSON string representation of the object
print(ChatCompletionToken.to_json())

# convert the object into a dict
chat_completion_token_dict = chat_completion_token_instance.to_dict()
# create an instance of ChatCompletionToken from a dict
chat_completion_token_from_dict = ChatCompletionToken.from_dict(chat_completion_token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
