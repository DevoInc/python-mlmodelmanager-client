Client Object
=============

This section explains how to use a client to manage the models of a ML Model
Manager server.


Create
------

To use a :class:`Client <devo_ml.modelmanager.Client>` you need the URL of the
ML Model Manager server and an authentication based on a token.

.. code-block::

    >>> from devo_ml.modelmanager import Client
    >>> from devo_ml.modelmanager.auth import HttpDevoStandAloneTokenAuth
    >>>
    >>> auth = HttpDevoStandAloneTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = Client("http://localhost", auth)
    >>> client
    <devo_ml.modelmanager._client.Client object at 0x7fa773450490>

Now you have a :class:`Client <devo_ml.modelmanager.Client>` ready to use to
manage models of the server `http://localhost`.

.. warning::

    The token used above is not a valid token, don't try to use with a real
    server.

Don't worry about :ref:`authentication <Authentication>`, we'll get into it a
bit later. Just be aware that we have created a client with the Devo's
``standAloneToken`` token scheme to authenticate, which is the default
authentication method.

In this example we don't tell the client to use any
:ref:`downloader <Downloaders>` via the constructor keyword `downloader`. In
that case a
:class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`
will be used as a fallback downloader with the current directory as path.
Neither you don't need to worry about downloaders right now because most of the
time the default downloader is fine, but you could create a client with your
customize downloader.

.. code-block::

    >>> ...
    >>> from devo_ml.modelmanager.downloader import FileSystemDownloader
    >>> ...
    >>> downloader = FileSystemDownloader("~/download/models")
    >>> client = Client("http://localhost", auth, downloader=downloader)
    >>>

Additionally the client accept a set of keywords that will be passing to the
underlying requests call. These keywords are the supported options by the
:doc:`Requests <requests:index>` library. For example, to set a `timeout`
you could do:

.. code-block::

    >>> ...
    >>> client = Client("http://localhost", auth, timeout=45)
    >>>

.. note::

    A default `timeout` of `30s` is used by the client.

What domain I am connecting to?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As you may have noticed in the example above it has not been indicated which
domain we want to connect to the client.

Since version ``2.4.0`` and above of the ML Model Manager server the domain
is inferred from the access token, therefore, the token you use in the
authentication will establish the domain you are connecting to.

.. note::

    To learn more about tokens and how to get one visit the
    `DEVO [.docs] <https://docs.devo.com/space/latest/94763821/Authentication+tokens>`_


Adding Models
-------------

The most frequent operation a data scientist will do with the client is
probably to add theirs models once they have been implemented, optimized,
trained, validated...

:meth:`Client.add_model <devo_ml.modelmanager.Client.add_model>` allows you to
create new models.

Parameters:

* **name**: The name of the model.
* **engine**: The engine of the model.
* **model_file**: The file path to the model file.
* **description** *(Optional)*: A brief description of the model. Defaults to ``None``
* **force** *(Optional)*: Whether to override the model. Defaults to ``False``.

.. code-block::

    >>> client.add_model(
    ...     "pokemon_onnx_regression",          # name
    ...     "ONNX",                             # engine
    ...     "~/models/pokemon.onnx",            # model_file
    ...     description="A funny Pokemon prediction"
    ... )
    >>>

If the model you are trying to add already exists in the system, a
:exc:`ModelAlreadyExists <devo_ml.modelmanager.error.ModelAlreadyExists>` error
will be thrown.

.. code-block::

    >>> client.add_model("existing_model_name", "H2O", "~/models/m.json")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../devo_ml/modelmanager/client.py", line 67, in add_model
        raise ModelAlreadyExists(name)
    devo_ml.modelmanager.error.ModelAlreadyExists: 'existing_model_name'
    >>>

This is correct, as it is not possible to add a model with the same name as an
existing one. But, if you would like or need to overwrite a model, you can do it.
You just have to specify it explicitly with ``force`` parameter set to ``True``,
e.g.:

.. code-block::

    >>> client.add_model("pokemon_onnx_regression", "ONNX", "~/models/pokemon.onnx", force=True)
    >>>

The `force` parameter, tells the system that we want to add the model and in
case it already exists, update it. Note that only the fields: `engine,
description (if anything other than None is passed) and the model file` will be
updated. The rest of the model fields are auto calculated or inferred by the
system and it is not possible to set an arbitrary value by the user.

.. note::

    It is the user's responsibility to ensure the match between the specified
    engine and the uploaded file. Note that the engine tells the system how to
    process the file.


Querying Models
---------------

Other operation that is usually of interest is to query the data of a model.

:meth:`Client.get_model <devo_ml.modelmanager.Client.get_model>` allows you to
query the data of an existing model.

Parameters:

* **name**: Name of the model to query.
* **download_file** *(Optional)*: Whether download the model file. Defaults to ``None``.

.. code-block::

    >>> client.get_model("pokemon_onnx_regression")
    {
       'id': 35,
       'name': 'pokemon_onnx_regression',
       'engine': 'ONNX',
       'description': 'A funny Pokemon prediction',
       ...
    }
    >>>

If the model you are trying to query does not exists, a
:exc:`ModelNotFound <devo_ml.modelmanager.error.ModelNotFound>` error will be thrown.

.. code-block::

    >>> client.get_model("non_existing_model_name")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../devo_ml/modelmanager/client.py", line 42, in get_model
        raise ModelNotFound(name)
    devo_ml.modelmanager.error.ModelNotFound: 'non_existing_model_name'
    >>>

The `download_file` parameter sets whether to download the model file through
the inner :ref:`downloader <Downloaders>` of the client.

.. code-block::

    >>> client.get_model("pokemon_onnx_regression", download_file=True)
    ...

:meth:`Client.find_model <devo_ml.modelmanager.Client.find_model>` is an alternative
to get a model. It behaves the same as `get_model` except it returns ``None``
instead of throw an error if the model doesn't exists. It is a convenient way to
get the model data without the need of catching errors.

Parameters:

* **name**: Name of the model to query.
* **download_file** *(Optional)*: Whether download the model file. Defaults to ``None``.

.. code-block::

    >>> client.find_model("non_existing_model_name")
    >>>


:meth:`Client.get_models <devo_ml.modelmanager.Client.get_models>` allows you
retrieve a list of all the models in the system. Note that `get_models` doesn't
allow downloading model files.

.. code-block::

    >>> client.get_models()
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


Legacy Client
-------------

In order to access servers prio to ``2.4.0`` you must use the
:class:`LegacyClient <devo_ml.modelmanager.LegacyClient>`. This is due to these
servers can't inferred the domain from the access token, so we need to pass it
in the constructor.

.. code-block::

    >>> from devo_ml.modelmanager import LegacyClient
    >>> from devo_ml.modelmanager.auth import HttpDevoStandAloneTokenAuth
    >>>
    >>> auth = HttpDevoStandAloneTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = LegacyClient("http://localhost", "self", auth)
    >>> client
    <devo_ml.modelmanager._client.LegacyClient object at 0x7fa773450490>

Note that we are connecting the client to the domain ``self`` not matter the
domain referred by the token.

All explained for the :class:`Client <devo_ml.modelmanager.Client>` is applicable
to the :class:`LegacyClient <devo_ml.modelmanager.LegacyClient>`, both expose the
same interface to the user in order to adding and querying models.

How do I know which client to use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are not sure which client to use you can start by using the
:class:`Client <devo_ml.modelmanager.Client>` and verify that you can get the
models without errors. If a
:exc:`ModelManagerError[404] <devo_ml.modelmanager.error.ModelManagerError>` is
thrown it means that the server doesn't support the endpoints accessed by the client
and you need to use the :class:`LegacyClient <devo_ml.modelmanager.LegacyClient>`
passing in the target domain.

.. code-block::

    >>> from devo_ml.modelmanager import Client
    >>> from devo_ml.modelmanager.auth import HttpDevoStandAloneTokenAuth
    >>>
    >>> auth = HttpDevoStandAloneTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = Client("http://localhost", auth)
    >>> client.get_models()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File ".../devo_ml/modelmanager/client.py", line 34, in get_models
        return self.api.get(self.endpoints.models())
      File ".../devo_ml/modelmanager/api.py", line 89, in __call__
        validate_or_raise_error(response.status_code, decoded_response)
      File ".../devo_ml/modelmanager/api.py", line 40, in validate_or_raise_error
        raise ModelManagerError.from_code(
    devo_ml.modelmanager.error.ModelManagerError: 404: HTTP 404 Not Found
    >>>


Factories
---------

To simplify the creation of clients, the library provides functions that allow
you to create clients with the most commonly used configurations in a single
step.

Create Client From Token
^^^^^^^^^^^^^^^^^^^^^^^^

The factory
:func:`create_client_from_token <devo_ml.modelmanager.create_client_from_token>`
allows you to create a ready to use :class:`Client <devo_ml.modelmanager.Client>`
when you have a valid access token.

Instead of this:

.. code-block::

    >>> from devo_ml.modelmanager import Client
    >>> from devo_ml.modelmanager.auth import HttpDevoStandAloneTokenAuth
    >>>
    >>> auth = HttpDevoStandAloneTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = Client("http://localhost", auth)

You could do a cleaner one line code:

.. code-block::

    >>> from devo_ml.modelmanager import create_client_from_token

    >>> client = create_client_from_token("http://localhost", "8a3vf98ai28sar1234lkj2l43td6f89a")

This creates a :class:`Client <devo_ml.modelmanager.Client>` to `http://localhost`
with Devo's ``standAloneToken`` token authentication.

You can set the type of authentication to use in the parameter `auth_type`.

* ``standalone`` to use :class:`HttpDevoStandAloneTokenAuth <devo_ml.modelmanager.auth.HttpDevoStandAloneTokenAuth>` *(default)*.
* ``bearer`` to use :class:`HttpDevoBearerTokenAuth <devo_ml.modelmanager.auth.HttpDevoBearerTokenAuth>`.

.. note::

    You can use constants rather than literals;
    :const:`STANDALONE <devo_ml.modelmanager.auth.STANDALONE>` or
    :const:`BEARER <devo_ml.modelmanager.auth.BEARER>`.

The `download_path` parameter allows you to setup the client downloader, but
note that you cannot use your own downloaders when creating clients with the
factory. A :class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`
is used as the downloader.

You can also use keywords to tune the underlying request.

.. code-block::

    >>> from devo_ml.modelmanager.auth import BEARER
    >>> from devo_ml.modelmanager import create_client_from_token

    >>> client = create_client_from_token(
    ...     "https://testing_url",                  # url
    ...     "8a3vf98ai28sar1234lkj2l43td6f89a",     # token
    ...     auth_type=BEARER,
    ...     download_path="~/models",
    ...     timeout=45
    ... )

Create Client From Profile
^^^^^^^^^^^^^^^^^^^^^^^^^^

The factory
:func:`create_client_from_profile <devo_ml.modelmanager.create_client_from_profile>`
allows you to setup several client configurations in one place and instantiate one
of those easily. It is useful when you have for example many environments you want to access.

.. code-block::

    >>> from devo_ml.modelmanager import create_client_from_profile

    >>> client = create_client_from_profile("testing", path="profiles.ini")

In this case we are telling the factory to create a
:class:`Client <devo_ml.modelmanager.Client>` based on the profile `testing`
located in the file `profiles.ini` of the current directory.

The parameter `path` not only accepts file names, it could be; a file name e.g.
`profiles.ini`, a file path e.g. `~/ml/config/profiles.ini` or a path e.g:
`~/ml/config`. Whatever the value is, the factory knows how to deal with it.

If you noticed, the parameter `path` is optional, so how does the factory know
where to look for a profile file if the path is not provided?. This is thanks
to the predefined set of paths where to look for the file.

The factory has two predefined paths where to look for a profile file;
the current directory and the user's home directory. It also adds the path
provided, if any. So the sequence of directories to look for a profile file is:

    * `path` if provided.
    * current directory, ``.``.
    * user's home directory, ``/home/<user>/``.

If `path` referrer a file name it will search for that file in every directory
of the set of paths, otherwise if it referrer a path it perform the same
process using `modelmanager.ini` as a file name. In this way you could just
create a file `modelmanager.ini` with your profiles, place it in the current
directory or in your home directory and create a client without the param
`path`. You can also use keywords to tune the underlying request.

.. code-block::

    >>> from devo_ml.modelmanager import create_client_from_profile

    >>> client = create_client_from_profile("testing", timeout=45)

What are the profile files like?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Profiles files are INI files compatible with the built-int Python
:doc:`ConfigParser <python:library/configparser>` module, capable of parsing
a kind of `Microsoft Windows INI` files. Let's see an example.

.. code-block:: ini

    [dev]
    url = https://dev_url
    token = 8a3vf98ai28sar1234lkj2l43td6f89a
    auth_type = standalone
    download_path = ~/models

    [testing]
    url = https://testing_url
    token = 26ab4c69f641bd3622a3b59bc09f781c
    auth_type = standalone
    download_path = ~/models

We have defined two profiles: `dev` and `testing`. Each of them have a set of
allowed attributes:

    * **url**: The URL of the server.
    * **token**: The access token to authenticate.
    * **auth_type** *(Optional)*: The auth type; ``standalone`` or ``bearer``. Defaults to ``standalone``.
    * | **download_path** *(Optional)*: The path to download model files. Fallback
        in the default downloader if is not provided.

You can setup as many profiles as you want as they are referrer by name.

The `download_path` profile attribute allows you to setup the client downloader,
but note that you cannot use your own downloaders when creating clients with the
factory. A :class:`FileSystemDownloader <devo_ml.modelmanager.downloader.FileSystemDownloader>`
is used as the downloader.

.. warning::

    Note the lack of quotes surrounding the values. Putting them will be an
    error or unwanted values.

.. note::

    You can use ``:`` instead of ``=`` as attribute `key-value` separator,
    they are interchangeable.
