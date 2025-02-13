# CompletionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | A string providing context for the model to complete. |
**model** | [**CompletionRequestModel**](CompletionRequestModel.md) |  |
**max_tokens** | **int** | The maximum number of tokens to generate. | [optional]
**stop** | **List[str]** | A list of string sequences that will truncate (stop) inference text output. For example, \&quot;&lt;/s&gt;\&quot; will stop generation as soon as the model generates the given token. | [optional]
**temperature** | **float** | A decimal number from 0-1 that determines the degree of randomness in the response. A temperature less than 1 favors more correctness and is appropriate for question answering or summarization. A value closer to 1 introduces more randomness in the output. | [optional]
**top_p** | **float** | A percentage (also called the nucleus parameter) that&#39;s used to dynamically adjust the number of choices for each predicted token based on the cumulative probabilities. It specifies a probability threshold below which all less likely tokens are filtered out. This technique helps maintain diversity and generate more fluent and natural-sounding text. | [optional]
**top_k** | **int** | An integer that&#39;s used to limit the number of choices for the next predicted word or token. It specifies the maximum number of tokens to consider at each step, based on their probability of occurrence. This technique helps to speed up the generation process and can improve the quality of the generated text by focusing on the most likely options. | [optional]
**repetition_penalty** | **float** | A number that controls the diversity of generated text by reducing the likelihood of repeated sequences. Higher values decrease repetition. | [optional]
**stream** | **bool** | If true, stream tokens as Server-Sent Events as the model generates them instead of waiting for the full model response. The stream terminates with &#x60;data: [DONE]&#x60;. If false, return a single JSON object containing the results. | [optional]
**logprobs** | **int** | Determines the number of most likely tokens to return at each token position log probabilities to return. | [optional]
**echo** | **bool** | If true, the response will contain the prompt. Can be used with &#x60;logprobs&#x60; to return prompt logprobs. | [optional]
**n** | **int** | The number of completions to generate for each prompt. | [optional]
**safety_model** | [**CompletionRequestSafetyModel**](CompletionRequestSafetyModel.md) |  | [optional]
**min_p** | **float** | A number between 0 and 1 that can be used as an alternative to top-p and top-k. | [optional]
**presence_penalty** | **float** | A number between -2.0 and 2.0 where a positive value increases the likelihood of a model talking about new topics. | [optional]
**frequency_penalty** | **float** | A number between -2.0 and 2.0 where a positive value decreases the likelihood of repeating tokens that have already been mentioned. | [optional]
**logit_bias** | **Dict[str, float]** | Adjusts the likelihood of specific tokens appearing in the generated output. | [optional]
**seed** | **int** | Seed value for reproducibility. | [optional]

## Example

```python
from together.generated.models.completion_request import CompletionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CompletionRequest from a JSON string
completion_request_instance = CompletionRequest.from_json(json)
# print the JSON string representation of the object
print(CompletionRequest.to_json())

# convert the object into a dict
completion_request_dict = completion_request_instance.to_dict()
# create an instance of CompletionRequest from a dict
completion_request_from_dict = CompletionRequest.from_dict(completion_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
