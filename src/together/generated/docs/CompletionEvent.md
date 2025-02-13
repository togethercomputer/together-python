# CompletionEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**CompletionChunk**](CompletionChunk.md) |  |

## Example

```python
from together.generated.models.completion_event import CompletionEvent

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionEvent from a JSON string
completion_event_instance = CompletionEvent.from_json(json)
# print the JSON string representation of the object
print(CompletionEvent.to_json())

# convert the object into a dict
completion_event_dict = completion_event_instance.to_dict()
# create an instance of CompletionEvent from a dict
completion_event_from_dict = CompletionEvent.from_dict(completion_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
