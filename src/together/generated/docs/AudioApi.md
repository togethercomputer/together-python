# together.generated.AudioApi

All URIs are relative to *https://api.together.xyz/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**audio_speech**](AudioApi.md#audio_speech) | **POST** /audio/speech | Create audio generation request


# **audio_speech**
> bytearray audio_speech(audio_speech_request=audio_speech_request)

Create audio generation request

Generate audio from input text

### Example

* Bearer Authentication (bearerAuth):

```python
import together.generated
from together.generated.models.audio_speech_request import AudioSpeechRequest
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
    api_instance = together.generated.AudioApi(api_client)
    audio_speech_request = together.generated.AudioSpeechRequest() # AudioSpeechRequest |  (optional)

    try:
        # Create audio generation request
        api_response = await api_instance.audio_speech(audio_speech_request=audio_speech_request)
        print("The response of AudioApi->audio_speech:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AudioApi->audio_speech: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **audio_speech_request** | [**AudioSpeechRequest**](AudioSpeechRequest.md)|  | [optional]

### Return type

**bytearray**

### Authorization

[bearerAuth](../README.md#bearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/octet-stream, audio/wav, audio/mpeg, text/event-stream, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | BadRequest |  -  |
**429** | RateLimit |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
