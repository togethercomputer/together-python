# FinetuneResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  |
**training_file** | **str** |  | [optional]
**validation_file** | **str** |  | [optional]
**model** | **str** |  | [optional]
**model_output_name** | **str** |  | [optional]
**model_output_path** | **str** |  | [optional]
**trainingfile_numlines** | **int** |  | [optional]
**trainingfile_size** | **int** |  | [optional]
**created_at** | **str** |  | [optional]
**updated_at** | **str** |  | [optional]
**n_epochs** | **int** |  | [optional]
**n_checkpoints** | **int** |  | [optional]
**n_evals** | **int** |  | [optional]
**batch_size** | **int** |  | [optional]
**learning_rate** | **float** |  | [optional]
**lr_scheduler** | [**LRScheduler**](.md) |  | [optional]
**warmup_ratio** | **float** |  | [optional]
**max_grad_norm** | **float** |  | [optional]
**weight_decay** | **float** |  | [optional]
**eval_steps** | **int** |  | [optional]
**train_on_inputs** | [**FinetuneResponseTrainOnInputs**](FinetuneResponseTrainOnInputs.md) |  | [optional]
**training_type** | [**FineTunesPostRequestTrainingType**](FineTunesPostRequestTrainingType.md) |  | [optional]
**status** | [**FinetuneJobStatus**](FinetuneJobStatus.md) |  |
**job_id** | **str** |  | [optional]
**events** | [**List[FineTuneEvent]**](FineTuneEvent.md) |  | [optional]
**token_count** | **int** |  | [optional]
**param_count** | **int** |  | [optional]
**total_price** | **int** |  | [optional]
**epochs_completed** | **int** |  | [optional]
**queue_depth** | **int** |  | [optional]
**wandb_project_name** | **str** |  | [optional]
**wandb_url** | **str** |  | [optional]

## Example

```python
from together.generated.models.finetune_response import FinetuneResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FinetuneResponse from a JSON string
finetune_response_instance = FinetuneResponse.from_json(json)
# print the JSON string representation of the object
print(FinetuneResponse.to_json())

# convert the object into a dict
finetune_response_dict = finetune_response_instance.to_dict()
# create an instance of FinetuneResponse from a dict
finetune_response_from_dict = FinetuneResponse.from_dict(finetune_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
