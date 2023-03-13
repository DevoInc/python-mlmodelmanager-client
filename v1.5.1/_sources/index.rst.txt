Devo ML Model Manager Client
============================

The **ML Model Manager** is a service to register machine learning models on
`Devo <https://www.devo.com>`_ platform. These models can be used through the
query engine using the ``mlevalmodel(...)`` operation or through the
`FLOW <https://docs.devo.com/space/latest/95213164/Flow>`_ correlation engine
including in the context the
`MlSingleModelEval <https://docs.devo.com/space/latest/95214962/ML+Single+Model+Evaluator>`_
unit.

devo-mlmodelmanager provides an easy-to-use client for Devo’s ML Model
Manager. Built on top of the widely used :doc:`Requests <requests:index>`
library exposes a simplified interface for model management, allowing you to
focus on the machine learning workflows and not worry about the integration
with Devo platform.

A quick example
---------------

That easy is to create a client:

    >>> from devo_ml.modelmanager import create_client_from_token
    >>> client = create_client_from_token("https://the_url", "the_token")

Here we use a
:ref:`client factory <user_guide/client-object:Create Client From Token>`
to create a :ref:`client <user_guide/client-object:Client Object>` object,
this is a convenient way of create a client ready to use.

Now we can start manage our models, e.g. to get a model called
`pokemon_onnx_regression`:

    >>> client.get_model("pokemon_onnx_regression")
    {
       'id': 35,
       'name': 'pokemon_onnx_regression',
       'engine': 'ONNX',
       'description': 'A funny Pokemon prediction',
       ...
    }

This is a simple example of the ML Model Manager Client is capable of.
Explore the rest of the documentation to learn more.

.. toctree::
    :maxdepth: 2
    :caption: Contents

    user_guide/index
    tutorials/index
    api_reference/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
