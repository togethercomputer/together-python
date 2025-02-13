# ImagesGenerationsPostRequestModel

The model to use for image generation.<br> <br> [See all of Together AI's image models](https://docs.together.ai/docs/serverless-models#image-models)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------

## Example

```python
from together.generated.models.images_generations_post_request_model import ImagesGenerationsPostRequestModel

# TODO update the JSON string below
json = "{}"
# create an instance of ImagesGenerationsPostRequestModel from a JSON string
images_generations_post_request_model_instance = ImagesGenerationsPostRequestModel.from_json(json)
# print the JSON string representation of the object
print(ImagesGenerationsPostRequestModel.to_json())

# convert the object into a dict
images_generations_post_request_model_dict = images_generations_post_request_model_instance.to_dict()
# create an instance of ImagesGenerationsPostRequestModel from a dict
images_generations_post_request_model_from_dict = ImagesGenerationsPostRequestModel.from_dict(images_generations_post_request_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
