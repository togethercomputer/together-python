# together.generated.FilesApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**files_get**](FilesApi.md#files_get) | **GET** /files | List all files
[**files_id_content_get**](FilesApi.md#files_id_content_get) | **GET** /files/{id}/content | Get file contents
[**files_id_delete**](FilesApi.md#files_id_delete) | **DELETE** /files/{id} | Delete a file
[**files_id_get**](FilesApi.md#files_id_get) | **GET** /files/{id} | List file


# **files_get**
> FileList files_get()

List all files

List the metadata for all uploaded data files.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.file_list import FileList
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
    api_instance = together.generated.FilesApi(api_client)

    try:
        # List all files
        api_response = await api_instance.files_get()
        print("The response of FilesApi->files_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->files_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FileList**](FileList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of files |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **files_id_content_get**
> FileObject files_id_content_get(id)

Get file contents

Get the contents of a single uploaded data file.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.file_object import FileObject
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
    api_instance = together.generated.FilesApi(api_client)
    id = 'id_example' # str |

    try:
        # Get file contents
        api_response = await api_instance.files_id_content_get(id)
        print("The response of FilesApi->files_id_content_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->files_id_content_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**FileObject**](FileObject.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File content retrieved successfully |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **files_id_delete**
> FileDeleteResponse files_id_delete(id)

Delete a file

Delete a previously uploaded data file.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.file_delete_response import FileDeleteResponse
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
    api_instance = together.generated.FilesApi(api_client)
    id = 'id_example' # str |

    try:
        # Delete a file
        api_response = await api_instance.files_id_delete(id)
        print("The response of FilesApi->files_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->files_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**FileDeleteResponse**](FileDeleteResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **files_id_get**
> FileResponse files_id_get(id)

List file

List the metadata for a single uploaded data file.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.file_response import FileResponse
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
    api_instance = together.generated.FilesApi(api_client)
    id = 'id_example' # str |

    try:
        # List file
        api_response = await api_instance.files_id_get(id)
        print("The response of FilesApi->files_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilesApi->files_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**FileResponse**](FileResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | File retrieved successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
