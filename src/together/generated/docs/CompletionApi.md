# together.generated.CompletionApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**completions**](CompletionApi.md#completions) | **POST** /completions | Create completion


# **completions**
> CompletionResponse completions(completion_request=completion_request)

Create completion

Query a language, code, or image model.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.completion_request import CompletionRequest
from together.generated.models.completion_response import CompletionResponse
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
    api_instance = together.generated.CompletionApi(api_client)
    completion_request = together.generated.CompletionRequest() # CompletionRequest |  (optional)

    try:
        # Create completion
        api_response = await api_instance.completions(completion_request=completion_request)
        print("The response of CompletionApi->completions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CompletionApi->completions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **completion_request** | [**CompletionRequest**](CompletionRequest.md)|  | [optional]

### Return type

[**CompletionResponse**](CompletionResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/event-stream

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
