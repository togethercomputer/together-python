# Pricing


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hourly** | **float** |  |
**input** | **float** |  |
**output** | **float** |  |
**base** | **float** |  |
**finetune** | **float** |  |

## Example

```python
from together.generated.models.pricing import Pricing

# TODO update the JSON string below
json = "{}"
# create an instance of Pricing from a JSON string
pricing_instance = Pricing.from_json(json)
# print the JSON string representation of the object
print(Pricing.to_json())

# convert the object into a dict
pricing_dict = pricing_instance.to_dict()
# create an instance of Pricing from a dict
pricing_from_dict = Pricing.from_dict(pricing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
