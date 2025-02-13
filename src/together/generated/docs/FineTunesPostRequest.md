# FineTunesPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**training_file** | **str** | File-ID of a training file uploaded to the Together API |
**validation_file** | **str** | File-ID of a validation file uploaded to the Together API | [optional]
**model** | **str** | Name of the base model to run fine-tune job on |
**n_epochs** | **int** | Number of epochs for fine-tuning | [optional] [default to 1]
**n_checkpoints** | **int** | Number of checkpoints to save during fine-tuning | [optional] [default to 1]
**n_evals** | **int** | Number of evaluations to be run on a given validation set during training | [optional] [default to 0]
**batch_size** | **int** | Batch size for fine-tuning | [optional] [default to 32]
**learning_rate** | **float** | Learning rate multiplier to use for training | [optional] [default to 0.000010]
**lr_scheduler** | [**LRScheduler**](.md) |  | [optional]
**warmup_ratio** | **float** | The percent of steps at the start of training to linearly increase the learning rate. | [optional] [default to 0.0]
**max_grad_norm** | **float** | Max gradient norm to be used for gradient clipping. Set to 0 to disable. | [optional] [default to 1.0]
**weight_decay** | **float** | Weight decay | [optional] [default to 0.0]
**suffix** | **str** | Suffix that will be added to your fine-tuned model name | [optional]
**wandb_api_key** | **str** | API key for Weights &amp; Biases integration | [optional]
**wandb_base_url** | **str** | The base URL of a dedicated Weights &amp; Biases instance. | [optional]
**wandb_project_name** | **str** | The Weights &amp; Biases project for your run. If not specified, will use &#x60;together&#x60; as the project name. | [optional]
**wandb_name** | **str** | The Weights &amp; Biases name for your run. | [optional]
**train_on_inputs** | [**FineTunesPostRequestTrainOnInputs**](FineTunesPostRequestTrainOnInputs.md) |  | [optional] [default to False]
**training_type** | [**FineTunesPostRequestTrainingType**](FineTunesPostRequestTrainingType.md) |  | [optional]

## Example

```python
from together.generated.models.fine_tunes_post_request import FineTunesPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FineTunesPostRequest from a JSON string
fine_tunes_post_request_instance = FineTunesPostRequest.from_json(json)
# print the JSON string representation of the object
print(FineTunesPostRequest.to_json())

# convert the object into a dict
fine_tunes_post_request_dict = fine_tunes_post_request_instance.to_dict()
# create an instance of FineTunesPostRequest from a dict
fine_tunes_post_request_from_dict = FineTunesPostRequest.from_dict(fine_tunes_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
