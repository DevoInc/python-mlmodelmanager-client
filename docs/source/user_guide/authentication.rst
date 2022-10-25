Authentication
==============

An authentication is a callable of the type
:const:`AuthCallable <devo_ml.modelmanager.auth.AuthCallable>` that receive a
request, perform an action to authenticate that request and return the
authenticated request.

An authenticated request must have a valid token in an HTML header with one of
the supported authentication methods; :ref:`StandAloneToken scheme` or
:ref:`Bearer scheme`. The library provides implementations for both
authentication methods.

.. note::

    To learn more about tokens and how to get one visit the
    `DEVO [.docs] <https://docs.devo.com/space/latest/94763821/Authentication+tokens>`_


StandAloneToken scheme
----------------------

StandAloneToken scheme is implemented in
:class:`HttpDevoStandAloneTokenAuth <devo_ml.modelmanager.auth.HttpDevoStandAloneTokenAuth>`.

It adds an HTML header with this template:

.. code:: text

    standAloneToken: <token>

This is how you can use this authentication:

.. code::

    >>> from devo_ml.modelmanager import Client
    >>> from devo_ml.modelmanager.auth import HttpDevoStandAloneTokenAuth

    >>> auth = HttpDevoStandAloneTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = Client("http://localhost", auth)


Bearer scheme
-------------

Bearer scheme is implemented in
:class:`HttpDevoBearerTokenAuth <devo_ml.modelmanager.auth.HttpDevoBearerTokenAuth>`.

It adds an HTML header with this template:

.. code:: text

    Authorization: Bearer <token>

This is how you can use this authentication:

.. code::

    >>> from devo_ml.modelmanager import Client
    >>> from devo_ml.modelmanager.auth import HttpDevoBearerTokenAuth

    >>> auth = HttpDevoBearerTokenAuth("8a3vf98ai28sar1234lkj2l43td6f89a")
    >>> client = Client("http://localhost", auth)


Authentication Factory
----------------------

With the authentication factory
:func:`create_auth_from_token <devo_ml.modelmanager.auth.create_auth_from_token>`
you can create the appropriate authentication.

.. code::

    >>> from devo_ml.modelmanager.auth import create_auth_from_token

    >>> auth = create_auth_from_token("8a3vf98ai28sar1234lkj2l43td6f89a", auth_type="bearer")
    >>> type(auth)
    <class 'devo_ml.modelmanager.auth.HttpDevoBearerTokenAuth'>

you can use constants instead of literal for the auth_type;
:class:`STANDALONE <devo_ml.modelmanager.auth.STANDALONE>` or
:class:`BEARER <devo_ml.modelmanager.auth.BEARER>`
