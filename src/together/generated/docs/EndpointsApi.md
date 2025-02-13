# together.generated.EndpointsApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_endpoint**](EndpointsApi.md#create_endpoint) | **POST** /endpoints | Create a dedicated endpoint, it will start automatically
[**delete_endpoint**](EndpointsApi.md#delete_endpoint) | **DELETE** /endpoints/{endpointId} | Delete endpoint
[**get_endpoint**](EndpointsApi.md#get_endpoint) | **GET** /endpoints/{endpointId} | Get endpoint by ID
[**list_endpoints**](EndpointsApi.md#list_endpoints) | **GET** /endpoints | List all endpoints, can be filtered by type
[**update_endpoint**](EndpointsApi.md#update_endpoint) | **PATCH** /endpoints/{endpointId} | Update endpoint, this can also be used to start or stop a dedicated endpoint


# **create_endpoint**
> DedicatedEndpoint create_endpoint(create_endpoint_request)

Create a dedicated endpoint, it will start automatically

Creates a new dedicated endpoint for serving models. The endpoint will automatically start after creation. You can deploy any supported model on hardware configurations that meet the model's requirements.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.create_endpoint_request import CreateEndpointRequest
from together.generated.models.dedicated_endpoint import DedicatedEndpoint
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
    api_instance = together.generated.EndpointsApi(api_client)
    create_endpoint_request = together.generated.CreateEndpointRequest() # CreateEndpointRequest |

    try:
        # Create a dedicated endpoint, it will start automatically
        api_response = await api_instance.create_endpoint(create_endpoint_request)
        print("The response of EndpointsApi->create_endpoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EndpointsApi->create_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_endpoint_request** | [**CreateEndpointRequest**](CreateEndpointRequest.md)|  |

### Return type

[**DedicatedEndpoint**](DedicatedEndpoint.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**403** | Unauthorized |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_endpoint**
> delete_endpoint(endpoint_id)

Delete endpoint

Permanently deletes an endpoint. This action cannot be undone.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
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
    api_instance = together.generated.EndpointsApi(api_client)
    endpoint_id = 'endpoint-d23901de-ef8f-44bf-b3e7-de9c1ca8f2d7' # str | The ID of the endpoint to delete

    try:
        # Delete endpoint
        await api_instance.delete_endpoint(endpoint_id)
    except Exception as e:
        print("Exception when calling EndpointsApi->delete_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_id** | **str**| The ID of the endpoint to delete |

### Return type

void (empty response body)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content - Endpoint successfully deleted |  -  |
**403** | Unauthorized |  -  |
**404** | Not Found |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_endpoint**
> DedicatedEndpoint get_endpoint(endpoint_id)

Get endpoint by ID

Retrieves details about a specific endpoint, including its current state, configuration, and scaling settings.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.dedicated_endpoint import DedicatedEndpoint
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
    api_instance = together.generated.EndpointsApi(api_client)
    endpoint_id = 'endpoint-d23901de-ef8f-44bf-b3e7-de9c1ca8f2d7' # str | The ID of the endpoint to retrieve

    try:
        # Get endpoint by ID
        api_response = await api_instance.get_endpoint(endpoint_id)
        print("The response of EndpointsApi->get_endpoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EndpointsApi->get_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_id** | **str**| The ID of the endpoint to retrieve |

### Return type

[**DedicatedEndpoint**](DedicatedEndpoint.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**403** | Unauthorized |  -  |
**404** | Not Found |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_endpoints**
> ListEndpoints200Response list_endpoints(type=type)

List all endpoints, can be filtered by type

Returns a list of all endpoints associated with your account. You can filter the results by type (dedicated or serverless).

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.list_endpoints200_response import ListEndpoints200Response
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
    api_instance = together.generated.EndpointsApi(api_client)
    type = 'dedicated' # str | Filter endpoints by type (optional)

    try:
        # List all endpoints, can be filtered by type
        api_response = await api_instance.list_endpoints(type=type)
        print("The response of EndpointsApi->list_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EndpointsApi->list_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| Filter endpoints by type | [optional]

### Return type

[**ListEndpoints200Response**](ListEndpoints200Response.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**403** | Unauthorized |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_endpoint**
> DedicatedEndpoint update_endpoint(endpoint_id, update_endpoint_request)

Update endpoint, this can also be used to start or stop a dedicated endpoint

Updates an existing endpoint's configuration. You can modify the display name, autoscaling settings, or change the endpoint's state (start/stop).

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.dedicated_endpoint import DedicatedEndpoint
from together.generated.models.update_endpoint_request import UpdateEndpointRequest
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
    api_instance = together.generated.EndpointsApi(api_client)
    endpoint_id = 'endpoint-d23901de-ef8f-44bf-b3e7-de9c1ca8f2d7' # str | The ID of the endpoint to update
    update_endpoint_request = together.generated.UpdateEndpointRequest() # UpdateEndpointRequest |

    try:
        # Update endpoint, this can also be used to start or stop a dedicated endpoint
        api_response = await api_instance.update_endpoint(endpoint_id, update_endpoint_request)
        print("The response of EndpointsApi->update_endpoint:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EndpointsApi->update_endpoint: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **endpoint_id** | **str**| The ID of the endpoint to update |
 **update_endpoint_request** | [**UpdateEndpointRequest**](UpdateEndpointRequest.md)|  |

### Return type

[**DedicatedEndpoint**](DedicatedEndpoint.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | 200 |  -  |
**403** | Unauthorized |  -  |
**404** | Not Found |  -  |
**500** | Internal error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
