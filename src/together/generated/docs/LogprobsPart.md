# LogprobsPart


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token_ids** | **List[float]** | List of token IDs corresponding to the logprobs | [optional]
**tokens** | **List[str]** | List of token strings | [optional]
**token_logprobs** | **List[float]** | List of token log probabilities | [optional]

## Example

```python
from together.generated.models.logprobs_part import LogprobsPart

# TODO update the JSON string below
json = "{}"
# create an instance of LogprobsPart from a JSON string
logprobs_part_instance = LogprobsPart.from_json(json)
# print the JSON string representation of the object
print(LogprobsPart.to_json())

# convert the object into a dict
logprobs_part_dict = logprobs_part_instance.to_dict()
# create an instance of LogprobsPart from a dict
logprobs_part_from_dict = LogprobsPart.from_dict(logprobs_part_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
