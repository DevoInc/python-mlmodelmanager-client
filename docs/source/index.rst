Devo ML Model Manager
=====================

An easy-to-use client for Devos's Machine Learning Model Manager server.

Built on top of the widely used :doc:`Requests <requests:index>` library, it
takes advantage of all the features it provides and exposes a simplified
interface for manage models.

The main purpose of this library is to allow you focus in the machine learning
workflows and not worry about the integration with Devo's ML Model Manager.

A quick example
---------------

That easy is to create a client:

    >>> from devo_ml.modelmanager import create_client_from_token
    >>> client = create_client_from_token("https://the_url", "the_token")

Here we use a :ref:`client factory <Create Client From Token>` to create a
:ref:`client <Client Object>` object, this is a convenient
way of create a client ready to use.

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
