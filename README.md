# python-mlmodelmanager

An easy-to-use client for Devos’s Machine Learning Model Manager.

Built on top of the widely used Requests library, it takes advantage of all the 
features it provides and exposes a simplified interface for manage models.

The main purpose of this library is to allow you to focus in the machine learning 
workflows and not worry about the integration with Devo’s ML Model Manager.

## A simple example

``` python
from devo_ml.modelmanager import create_client_from_token

url = "<model-manager-server-url>"
token = "<valid-access-token>"

client = create_client_from_token(url, token)

client.add_model(
   "pokemon_onnx_regression",          # model name
   "ONNX",                             # model engine
   "~/models/pokemon.onnx",            # model file
   description="A funny Pokemon prediction"
)
```

## Requirements

* Python 3.7+

## Install

``` console
$ pip install devo-mlmodelmanager
```

## Documentation

Explore the [documentation](https://devoinc.github.io/python-mlmodelmanager-client/) to learn more.
