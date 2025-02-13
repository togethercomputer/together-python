# FinetuneDownloadResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  | [optional]
**id** | **str** |  | [optional]
**checkpoint_step** | **int** |  | [optional]
**filename** | **str** |  | [optional]
**size** | **int** |  | [optional]

## Example

```python
from together.generated.models.finetune_download_result import FinetuneDownloadResult

# TODO update the JSON string below
json = "{}"
# create an instance of FinetuneDownloadResult from a JSON string
finetune_download_result_instance = FinetuneDownloadResult.from_json(json)
# print the JSON string representation of the object
print(FinetuneDownloadResult.to_json())

# convert the object into a dict
finetune_download_result_dict = finetune_download_result_instance.to_dict()
# create an instance of FinetuneDownloadResult from a dict
finetune_download_result_from_dict = FinetuneDownloadResult.from_dict(finetune_download_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
