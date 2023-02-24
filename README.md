![License](https://img.shields.io/github/license/DevoInc/python-mlmodelmanager-client)
![Release](https://img.shields.io/github/v/release/DevoInc/python-mlmodelmanager-client?display_name=tag&sort=semver)
![Tests](https://github.com/DevoInc/python-mlmodelmanager-client/actions/workflows/test-tox.yml/badge.svg)
![Python](https://img.shields.io/pypi/pyversions/devo-mlmodelmanager)

# Devo Python ML Model Manager Client

The **ML Model Manager** is a service to register machine learning models on
[Devo](https://www.devo.com) platform. These models can be used through the
query engine using the `mlevalmodel(...)`  operation or through the
[FLOW](https://docs.devo.com/space/latest/95213164/Flow) correlation engine
including in the context the
[MlSingleModelEval](https://docs.devo.com/space/latest/95214962/ML+Single+Model+Evaluator)
unit.

**devo-mlmodelmanager** provides an easy-to-use client for Devo’s ML Model
Manager. Built on top of the widely used
[Requests](https://requests.readthedocs.io/en/latest/) library exposes a
simplified interface for model management, allowing you to focus in the machine
learning workflows and not worry about the integration with Devo platform.

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
