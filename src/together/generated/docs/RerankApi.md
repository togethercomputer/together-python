# together.generated.RerankApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**rerank**](RerankApi.md#rerank) | **POST** /rerank | Create a rerank request


# **rerank**
> RerankResponse rerank(rerank_request=rerank_request)

Create a rerank request

Query a reranker model

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.rerank_request import RerankRequest
from together.generated.models.rerank_response import RerankResponse
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
    api_instance = together.generated.RerankApi(api_client)
    rerank_request = together.generated.RerankRequest() # RerankRequest |  (optional)

    try:
        # Create a rerank request
        api_response = await api_instance.rerank(rerank_request=rerank_request)
        print("The response of RerankApi->rerank:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RerankApi->rerank: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **rerank_request** | [**RerankRequest**](RerankRequest.md)|  | [optional]

### Return type

[**RerankResponse**](RerankResponse.md)

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
