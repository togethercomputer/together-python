# together.generated.ChatApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_completions**](ChatApi.md#chat_completions) | **POST** /chat/completions | Create chat completion


# **chat_completions**
> ChatCompletionResponse chat_completions(chat_completion_request=chat_completion_request)

Create chat completion

Query a chat model.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.chat_completion_request import ChatCompletionRequest
from together.generated.models.chat_completion_response import ChatCompletionResponse
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
    api_instance = together.generated.ChatApi(api_client)
    chat_completion_request = together.generated.ChatCompletionRequest() # ChatCompletionRequest |  (optional)

    try:
        # Create chat completion
        api_response = await api_instance.chat_completions(chat_completion_request=chat_completion_request)
        print("The response of ChatApi->chat_completions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ChatApi->chat_completions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chat_completion_request** | [**ChatCompletionRequest**](ChatCompletionRequest.md)|  | [optional]

### Return type

[**ChatCompletionResponse**](ChatCompletionResponse.md)

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
