# CompletionToken


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  |
**text** | **str** |  |
**logprob** | **float** |  |
**special** | **bool** |  |

## Example

```python
from together.generated.models.completion_token import CompletionToken

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionToken from a JSON string
completion_token_instance = CompletionToken.from_json(json)
# print the JSON string representation of the object
print(CompletionToken.to_json())

# convert the object into a dict
completion_token_dict = completion_token_instance.to_dict()
# create an instance of CompletionToken from a dict
completion_token_from_dict = CompletionToken.from_dict(completion_token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
