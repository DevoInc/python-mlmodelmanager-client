Functions Facade
================

It is possible to manage the models of a ML Model Manager server trough
functions rather than trough an object
:class:`Client <devo_ml.modelmanager.client.Client>`.

The library provides a set of functions that expose the same interface as the
client object and allow operations to be performed in a single call.

Let’s overview the functions.


:func:`add_model(...) <devo_ml.modelmanager.func_facade.add_model>`
-------------------------------------------------------------------

Allows you to create a model.

.. code-block::

    >>> from devo_ml.modelmanager import add_model
    >>>
    >>> add_model(
    ...     "http://localhost",                         # url
    ...     "8a3vf98ai28sar1234lkj2l43td6f89a",         # token
    ...     "pokemon_onnx_regression",                  # model name
    ...     "ONNX",                                     # model engine
    ...     "~/models/pokemon.onnx",                    # model file
    ...     description="A funny Pokemon prediction"
    ... )
    >>>

If the model you are trying to add already exists in the system, a
:exc:`ModelAlreadyExists <devo_ml.modelmanager.error.ModelAlreadyExists>`
error will be thrown.

Trough the `force` parameter you can mange whether to override the model.


:func:`get_model(...) <devo_ml.modelmanager.func_facade.get_model>`
-------------------------------------------------------------------

Allows you to retrieve model.

.. code-block::

    >>> from devo_ml.modelmanager import get_model
    >>>
    >>> get_model(
    ...     "http://localhost",                         # url
    ...     "8a3vf98ai28sar1234lkj2l43td6f89a",         # token
    ...     "pokemon_onnx_regression",                  # model name
    ...     download_path="~/models",
    ... )
    {
       'id': 35,
       'name': 'pokemon_onnx_regression',
       'engine': 'ONNX',
       'description': 'A funny Pokemon prediction',
       ...
    }
    >>>

The parameter `download_path` indicates that we want download the model file,
and where we want to download the model file. Omitting this parameter will not
download file. Note that you can not use a custom downloader with
the function.

If the model you are trying to query does not exists, a
:exc:`ModelNotFound <devo_ml.modelmanager.error.ModelNotFound>`
error will be thrown.


:func:`find_model(...) <devo_ml.modelmanager.func_facade.find_model>`
---------------------------------------------------------------------

It behaves the same as `get_model(...)` except it returns ``None`` instead of
throw an error if the model doesn't exists. It is a convenient way to get the
model data without the need of catching errors.

.. code-block::

    >>> from devo_ml.modelmanager import find_model
    >>>
    >>> find_model(
    ...     "http://localhost",                         # url
    ...     "8a3vf98ai28sar1234lkj2l43td6f89a",         # token
    ...     "pokemon_onnx_regression",                  # model name
    ...     download_path="~/models",
    ... )
    {
       'id': 35,
       'name': 'pokemon_onnx_regression',
       'engine': 'ONNX',
       'description': 'A funny Pokemon prediction',
       ...
    }
    >>>


:func:`get_models(...) <devo_ml.modelmanager.func_facade.get_models>`
---------------------------------------------------------------------

Allows you retrieve a list of all the models in the system. Note that it doesn't
allow downloading model files.

.. code-block::

    >>> from devo_ml.modelmanager import get_models
    >>>
    >>> get_models(
    ...     "http://localhost",                         # url
    ...     "8a3vf98ai28sar1234lkj2l43td6f89a",         # token
    ... )
    [
        {
            'id': 35,
            'name': 'pokemon_onnx_regression',
            'engine': 'ONNX',
            'description': 'A funny Pokemon prediction',
            ...
        }, {
            'id': 36,
            'name': 'credit_card_gjp',
            'engine': 'H2O',
            'description': 'gjp model on credit card fraud dataset',
            ...
        }, {
        ...
    ]
    >>>


.. note::

    You can not use your own downloaders with the functions facade.

.. note::

    You can choose the authentication to use with the `auth_type` parameter and
    tune the underlying request with keywords. This is valid for all functions
    facade.
