# ImagesGenerationsPostRequestImageLorasInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** | The URL of the LoRA to apply (e.g. https://huggingface.co/strangerzonehf/Flux-Midjourney-Mix2-LoRA). |
**scale** | **float** | The strength of the LoRA&#39;s influence. Most LoRA&#39;s recommend a value of 1. |

## Example

```python
from together.generated.models.images_generations_post_request_image_loras_inner import ImagesGenerationsPostRequestImageLorasInner

# TODO update the JSON string below
json = "{}"
# create an instance of ImagesGenerationsPostRequestImageLorasInner from a JSON string
images_generations_post_request_image_loras_inner_instance = ImagesGenerationsPostRequestImageLorasInner.from_json(json)
# print the JSON string representation of the object
print(ImagesGenerationsPostRequestImageLorasInner.to_json())

# convert the object into a dict
images_generations_post_request_image_loras_inner_dict = images_generations_post_request_image_loras_inner_instance.to_dict()
# create an instance of ImagesGenerationsPostRequestImageLorasInner from a dict
images_generations_post_request_image_loras_inner_from_dict = ImagesGenerationsPostRequestImageLorasInner.from_dict(images_generations_post_request_image_loras_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
