# together.generated.HardwareApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_hardware**](HardwareApi.md#list_hardware) | **GET** /hardware | List available hardware configurations


# **list_hardware**
> ListHardware200Response list_hardware(model=model)

List available hardware configurations

Returns a list of available hardware configurations for deploying models. When a model parameter is provided, it returns only hardware configurations compatible with that model, including their current availability status.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.list_hardware200_response import ListHardware200Response
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
    api_instance = together.generated.HardwareApi(api_client)
    model = 'meta-llama/Llama-3-70b-chat-hf' # str | Filter hardware configurations by model compatibility (optional)

    try:
        # List available hardware configurations
        api_response = await api_instance.list_hardware(model=model)
        print("The response of HardwareApi->list_hardware:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling HardwareApi->list_hardware: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **model** | **str**| Filter hardware configurations by model compatibility | [optional]

### Return type

[**ListHardware200Response**](ListHardware200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of available hardware configurations |  -  |
**403** | Unauthorized |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
