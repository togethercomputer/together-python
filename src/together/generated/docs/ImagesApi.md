# together.generated.ImagesApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**images_generations_post**](ImagesApi.md#images_generations_post) | **POST** /images/generations | Create image


# **images_generations_post**
> ImageResponse images_generations_post(images_generations_post_request)

Create image

Use an image model to generate an image for a given prompt.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.image_response import ImageResponse
from together.generated.models.images_generations_post_request import ImagesGenerationsPostRequest
from together.generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.together.xyz/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = together.generated.Configuration(
    host = "https://api.together.xyz/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: bearerAuth
configuration = together.generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
async with together.generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = together.generated.ImagesApi(api_client)
    images_generations_post_request = together.generated.ImagesGenerationsPostRequest() # ImagesGenerationsPostRequest |

    try:
        # Create image
        api_response = await api_instance.images_generations_post(images_generations_post_request)
        print("The response of ImagesApi->images_generations_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ImagesApi->images_generations_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **images_generations_post_request** | [**ImagesGenerationsPostRequest**](ImagesGenerationsPostRequest.md)|  |

### Return type

[**ImageResponse**](ImageResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Image generated successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
