# makeijan_client.DefaultApi

All URIs are relative to *http://{host}:{port}/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_model_by_id**](DefaultApi.md#delete_model_by_id) | **DELETE** /domains/{domainName}/models/{name} | 
[**find_all**](DefaultApi.md#find_all) | **GET** /domains/{domainName}/models | 
[**find_all_children**](DefaultApi.md#find_all_children) | **GET** /domains/{domainName}/models/{name}/children | 
[**find_by_name**](DefaultApi.md#find_by_name) | **GET** /domains/{domainName}/models/{name} | 
[**find_by_name_fast**](DefaultApi.md#find_by_name_fast) | **GET** /domains/{domainName}/models/{name}/fast | 
[**find_filtered**](DefaultApi.md#find_filtered) | **GET** /domains/{domainName}/models/filtered | 
[**find_image**](DefaultApi.md#find_image) | **GET** /domains/{domainName}/models/{name}/image | 
[**find_newer_than**](DefaultApi.md#find_newer_than) | **GET** /domains/*/models/newerthan/{newerthan} |
[**save_model**](DefaultApi.md#save_model) | **POST** /domains/{domainName}/models | 
[**upload_model_image**](DefaultApi.md#upload_model_image) | **POST** /domains/{domainName}/models/images/upload | 

# **delete_model_by_id**
> delete_model_by_id(domain_name, name)



Delete a model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str | 

try:
    api_instance.delete_model_by_id(domain_name, name)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_model_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all**
> list[Model] find_all(domain_name)



List available models filtered by domain

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 

try:
    api_response = api_instance.find_all(domain_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_all: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 

### Return type

[**list[Model]**](Model.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_all_children**
> list[Model] find_all_children(domain_name, name)



List all models that are children of the passed model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str | 

try:
    api_response = api_instance.find_all_children(domain_name, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_all_children: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**list[Model]**](Model.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_by_name**
> ModelDetail find_by_name(domain_name, name)



Display detailed information about a model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str | 

try:
    api_response = api_instance.find_by_name(domain_name, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**ModelDetail**](ModelDetail.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_by_name_fast**
> ModelDetail find_by_name_fast(domain_name, name)



Display detailed information about a model without including the image binary

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str | 

try:
    api_response = api_instance.find_by_name_fast(domain_name, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_by_name_fast: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**ModelDetail**](ModelDetail.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_filtered**
> list[Model] find_filtered(domain_name, name=name, engine=engine)



Finds models in a given domain filtered by given parameters

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str |  (optional)
engine = 'engine_example' # str |  (optional)

try:
    api_response = api_instance.find_filtered(domain_name, name=name, engine=engine)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_filtered: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | [optional] 
 **engine** | **str**|  | [optional] 

### Return type

[**list[Model]**](Model.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_image**
> Image find_image(domain_name, name)



Get the binary image of a model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
name = 'name_example' # str | 

try:
    api_response = api_instance.find_image(domain_name, name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **name** | **str**|  | 

### Return type

[**Image**](Image.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **find_newer_than**
> list[Model] find_newer_than(newerthan)



Finds models updated after the given date on every domain

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
newerthan = 789 # int | 

try:
    api_response = api_instance.find_newer_than(newerthan)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->find_newer_than: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **newerthan** | **int**|  | 

### Return type

[**list[Model]**](Model.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **save_model**
> save_model(domain_name, body=body)



Save a model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
body = makeijan_client.ModelDetail() # ModelDetail |  (optional)

try:
    api_instance.save_model(domain_name, body=body)
except ApiException as e:
    print("Exception when calling DefaultApi->save_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **body** | [**ModelDetail**](ModelDetail.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_model_image**
> ModelReview upload_model_image(domain_name, engine=engine, file_name=file_name)



Upload the binary image of a model

### Example
```python
from __future__ import print_function
import time
import makeijan_client
from makeijan_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: standAloneToken
configuration = makeijan_client.Configuration()
configuration.api_key['standAloneToken'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['standAloneToken'] = 'Bearer'

# create an instance of the API class
api_instance = makeijan_client.DefaultApi(makeijan_client.ApiClient(configuration))
domain_name = 'domain_name_example' # str | 
engine = 'engine_example' # str |  (optional)
file_name = 'file_name_example' # str |  (optional)

try:
    api_response = api_instance.upload_model_image(domain_name, engine=engine, file_name=file_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->upload_model_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **domain_name** | **str**|  | 
 **engine** | **str**|  | [optional] 
 **file_name** | **str**|  | [optional] 

### Return type

[**ModelReview**](ModelReview.md)

### Authorization

[standAloneToken](../README.md#standAloneToken)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

