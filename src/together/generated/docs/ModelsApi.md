# together.generated.ModelsApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**models**](ModelsApi.md#models) | **GET** /models | List all models


# **models**
> List[ModelInfo] models()

List all models

Lists all of Together's open-source models

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.model_info import ModelInfo
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
    api_instance = together.generated.ModelsApi(api_client)

    try:
        # List all models
        api_response = await api_instance.models()
        print("The response of ModelsApi->models:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModelsApi->models: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ModelInfo]**](ModelInfo.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**400** | BadRequest |  -  |
**401** | Unauthorized |  -  |
**404** | NotFound |  -  |
**429** | RateLimit |  -  |
**504** | Timeout |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
