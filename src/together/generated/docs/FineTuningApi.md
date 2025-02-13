# together.generated.FineTuningApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**fine_tunes_get**](FineTuningApi.md#fine_tunes_get) | **GET** /fine-tunes | List all jobs
[**fine_tunes_id_cancel_post**](FineTuningApi.md#fine_tunes_id_cancel_post) | **POST** /fine-tunes/{id}/cancel | Cancel job
[**fine_tunes_id_events_get**](FineTuningApi.md#fine_tunes_id_events_get) | **GET** /fine-tunes/{id}/events | List job events
[**fine_tunes_id_get**](FineTuningApi.md#fine_tunes_id_get) | **GET** /fine-tunes/{id} | List job
[**fine_tunes_post**](FineTuningApi.md#fine_tunes_post) | **POST** /fine-tunes | Create job
[**finetune_download_get**](FineTuningApi.md#finetune_download_get) | **GET** /finetune/download | Download model


# **fine_tunes_get**
> FinetuneList fine_tunes_get()

List all jobs

List the metadata for all fine-tuning jobs.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.finetune_list import FinetuneList
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
    api_instance = together.generated.FineTuningApi(api_client)

    try:
        # List all jobs
        api_response = await api_instance.fine_tunes_get()
        print("The response of FineTuningApi->fine_tunes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->fine_tunes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**FinetuneList**](FinetuneList.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of fine-tune jobs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fine_tunes_id_cancel_post**
> FinetuneResponse fine_tunes_id_cancel_post(id)

Cancel job

Cancel a currently running fine-tuning job.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.finetune_response import FinetuneResponse
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
    api_instance = together.generated.FineTuningApi(api_client)
    id = 'id_example' # str | Fine-tune ID to cancel. A string that starts with `ft-`.

    try:
        # Cancel job
        api_response = await api_instance.fine_tunes_id_cancel_post(id)
        print("The response of FineTuningApi->fine_tunes_id_cancel_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->fine_tunes_id_cancel_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Fine-tune ID to cancel. A string that starts with &#x60;ft-&#x60;. |

### Return type

[**FinetuneResponse**](FinetuneResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully cancelled the fine-tuning job. |  -  |
**400** | Invalid request parameters. |  -  |
**404** | Fine-tune ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fine_tunes_id_events_get**
> FinetuneListEvents fine_tunes_id_events_get(id)

List job events

List the events for a single fine-tuning job.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.finetune_list_events import FinetuneListEvents
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
    api_instance = together.generated.FineTuningApi(api_client)
    id = 'id_example' # str |

    try:
        # List job events
        api_response = await api_instance.fine_tunes_id_events_get(id)
        print("The response of FineTuningApi->fine_tunes_id_events_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->fine_tunes_id_events_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**FinetuneListEvents**](FinetuneListEvents.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of fine-tune events |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fine_tunes_id_get**
> FinetuneResponse fine_tunes_id_get(id)

List job

List the metadata for a single fine-tuning job.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.finetune_response import FinetuneResponse
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
    api_instance = together.generated.FineTuningApi(api_client)
    id = 'id_example' # str |

    try:
        # List job
        api_response = await api_instance.fine_tunes_id_get(id)
        print("The response of FineTuningApi->fine_tunes_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->fine_tunes_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |

### Return type

[**FinetuneResponse**](FinetuneResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fine-tune job details retrieved successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fine_tunes_post**
> FinetuneResponse fine_tunes_post(fine_tunes_post_request)

Create job

Use a model to create a fine-tuning job.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.fine_tunes_post_request import FineTunesPostRequest
from together.generated.models.finetune_response import FinetuneResponse
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
    api_instance = together.generated.FineTuningApi(api_client)
    fine_tunes_post_request = together.generated.FineTunesPostRequest() # FineTunesPostRequest |

    try:
        # Create job
        api_response = await api_instance.fine_tunes_post(fine_tunes_post_request)
        print("The response of FineTuningApi->fine_tunes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->fine_tunes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fine_tunes_post_request** | [**FineTunesPostRequest**](FineTunesPostRequest.md)|  |

### Return type

[**FinetuneResponse**](FinetuneResponse.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fine-tuning job initiated successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **finetune_download_get**
> FinetuneDownloadResult finetune_download_get(ft_id, checkpoint_step=checkpoint_step, checkpoint=checkpoint, output=output)

Download model

Download a compressed fine-tuned model or checkpoint to local disk.

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.finetune_download_result import FinetuneDownloadResult
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
    api_instance = together.generated.FineTuningApi(api_client)
    ft_id = 'ft_id_example' # str | Fine-tune ID to download. A string that starts with `ft-`.
    checkpoint_step = 56 # int | Specifies step number for checkpoint to download. Ignores `checkpoint` value if set. (optional)
    checkpoint = 'checkpoint_example' # str | Specifies checkpoint type to download - `merged` vs `adapter`. This field is required if the checkpoint_step is not set. (optional)
    output = 'output_example' # str | Specifies output file name for downloaded model. Defaults to `$PWD/{model_name}.{extension}`. (optional)

    try:
        # Download model
        api_response = await api_instance.finetune_download_get(ft_id, checkpoint_step=checkpoint_step, checkpoint=checkpoint, output=output)
        print("The response of FineTuningApi->finetune_download_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FineTuningApi->finetune_download_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ft_id** | **str**| Fine-tune ID to download. A string that starts with &#x60;ft-&#x60;. |
 **checkpoint_step** | **int**| Specifies step number for checkpoint to download. Ignores &#x60;checkpoint&#x60; value if set. | [optional]
 **checkpoint** | **str**| Specifies checkpoint type to download - &#x60;merged&#x60; vs &#x60;adapter&#x60;. This field is required if the checkpoint_step is not set. | [optional]
 **output** | **str**| Specifies output file name for downloaded model. Defaults to &#x60;$PWD/{model_name}.{extension}&#x60;. | [optional]

### Return type

[**FinetuneDownloadResult**](FinetuneDownloadResult.md)

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully downloaded the fine-tuned model or checkpoint. |  -  |
**400** | Invalid request parameters. |  -  |
**404** | Fine-tune ID not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
