# ModelReview

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**valid** | **bool** | Indicates wether the model is valid or not | [optional] 
**error_detail** | **str** | String with some details about what could be wrong about an invaid model | [optional] 
**output_type** | **str** | The type of the value generated by the model as a prediction | [optional] 
**category** | **str** | The type of the model | [optional] 
**image_id** | **int** | The id of the uploaded image or file of the model | [optional] 
**fields** | [**list[Field]**](Field.md) | The fields or parameters that are consumed by the model | [optional] 
**clusters** | [**list[Cluster]**](Cluster.md) | For clustering models, the positions and names of the clusters | [optional] 
**file_name** | **str** | The name of the uploaded image file | [optional] 
**size** | **int** | The size of the uploaded image file | [optional] 
**runtime_size** | **int** | The size of the model while running in bytes | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
