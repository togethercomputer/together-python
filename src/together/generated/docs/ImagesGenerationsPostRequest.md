# ImagesGenerationsPostRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt** | **str** | A description of the desired images. Maximum length varies by model. |
**model** | [**ImagesGenerationsPostRequestModel**](ImagesGenerationsPostRequestModel.md) |  |
**steps** | **int** | Number of generation steps. | [optional] [default to 20]
**image_url** | **str** | URL of an image to use for image models that support it. | [optional]
**seed** | **int** | Seed used for generation. Can be used to reproduce image generations. | [optional]
**n** | **int** | Number of image results to generate. | [optional] [default to 1]
**height** | **int** | Height of the image to generate in number of pixels. | [optional] [default to 1024]
**width** | **int** | Width of the image to generate in number of pixels. | [optional] [default to 1024]
**negative_prompt** | **str** | The prompt or prompts not to guide the image generation. | [optional]
**response_format** | **str** | Format of the image response. Can be either a base64 string or a URL. | [optional]
**guidance** | **float** | Adjusts the alignment of the generated image with the input prompt. Higher values (e.g., 8-10) make the output more faithful to the prompt, while lower values (e.g., 1-5) encourage more creative freedom. | [optional] [default to 3.5]
**output_format** | **str** | The format of the image response. Can be either be &#x60;jpeg&#x60; or &#x60;png&#x60;. Defaults to &#x60;jpeg&#x60;. | [optional] [default to 'jpeg']
**image_loras** | [**List[ImagesGenerationsPostRequestImageLorasInner]**](ImagesGenerationsPostRequestImageLorasInner.md) | An array of objects that define LoRAs (Low-Rank Adaptations) to influence the generated image. | [optional]

## Example

```python
from together.generated.models.images_generations_post_request import ImagesGenerationsPostRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ImagesGenerationsPostRequest from a JSON string
images_generations_post_request_instance = ImagesGenerationsPostRequest.from_json(json)
# print the JSON string representation of the object
print(ImagesGenerationsPostRequest.to_json())

# convert the object into a dict
images_generations_post_request_dict = images_generations_post_request_instance.to_dict()
# create an instance of ImagesGenerationsPostRequest from a dict
images_generations_post_request_from_dict = ImagesGenerationsPostRequest.from_dict(images_generations_post_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
