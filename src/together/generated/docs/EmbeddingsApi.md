# together.generated.EmbeddingsApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**embeddings**](EmbeddingsApi.md#embeddings) | **POST** /embeddings | Create embedding


# **embeddings**
> EmbeddingsResponse embeddings(embeddings_request=embeddings_request)

Create embedding

Query an embedding model for a given string of text.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.embeddings_request import EmbeddingsRequest
from together.generated.models.embeddings_response import EmbeddingsResponse
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
    api_instance = together.generated.EmbeddingsApi(api_client)
    embeddings_request = together.generated.EmbeddingsRequest() # EmbeddingsRequest |  (optional)

    try:
        # Create embedding
        api_response = await api_instance.embeddings(embeddings_request=embeddings_request)
        print("The response of EmbeddingsApi->embeddings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EmbeddingsApi->embeddings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **embeddings_request** | [**EmbeddingsRequest**](EmbeddingsRequest.md)|  | [optional]

### Return type

[**EmbeddingsResponse**](EmbeddingsResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**400** | BadRequest |  -  |
**401** | Unauthorized |  -  |
**404** | NotFound |  -  |
**429** | RateLimit |  -  |
**503** | Overloaded |  -  |
**504** | Timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
