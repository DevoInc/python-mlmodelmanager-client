"""Supported authentication methods of ML Model Manager."""

from __future__ import annotations

import abc

from typing import Callable
from requests import PreparedRequest


#: Signature type for callable authentications.
AuthCallable = Callable[[PreparedRequest], PreparedRequest]

#: Constant denoting authentication type Bearer.
BEARER = "bearer"

#: Constant denoting authentication type StandAlone.
STANDALONE = "standalone"


def get_default_auth_type() -> str:
    """Returns the default authentication type used.

    :return: The default authentication
    """
    return STANDALONE


def validate_auth_type(auth_type: str) -> bool:
    """Checks whether a value is a valid authentication type.

    :param auth_type: The value to validate
    :return: ``True`` if the value is a valid authentication type otherwise
        ``False``
    """
    return auth_type in (BEARER, STANDALONE)


def create_auth_from_token(
    token: str,
    auth_type: str = STANDALONE
) -> AuthCallable:
    """Creates an authentication object based on a token ready to use
    by the client.

    :param token: The token to authenticate
    :param auth_type: The type of the authentication,
        defaults to :const:`STANDALONE`
    :raises ValueError: if ``auth_type`` is not valid
    :return: An authentication object
    """
    if not validate_auth_type(auth_type):
        raise ValueError(f"Invalid auth type: '{auth_type}'")
    return {
        BEARER: HttpDevoBearerTokenAuth,
        STANDALONE: HttpDevoStandAloneTokenAuth,
    }.get(auth_type, HttpDevoStandAloneTokenAuth)(token)


class HttpDevoTokenAuth(abc.ABC):
    """An HTTP authentication scheme based on a token supported by
    ML Model Manager.

    The implementations of this class are objects ready to use by the client to
    authenticate and also by :doc:`Requests <requests:user/authentication>`
    library.
    """

    def __init__(self, token: str) -> None:
        """Creates an authentication base on a token.

        :param token: The token used
        """
        self.token = token

    @abc.abstractmethod
    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        """Subclasses must implement this method to client be able to
        call it as a function when authenticate a request.

        :param req: The request object to authenticate
        :return: The request object authenticated
        """


class HttpDevoStandAloneTokenAuth(HttpDevoTokenAuth):
    """An :class:`HttpDevoTokenAuth` that authenticates a request with HTTP
    Devo Standalone authentication scheme.
    """

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        """Adds the header ``standAloneToken: <token>`` to the request.

        :param req: The request object to authenticate
        :return: The request object authenticated with proper header
        """
        req.headers['standAloneToken'] = self.token
        return req


class HttpDevoBearerTokenAuth(HttpDevoTokenAuth):
    """An :class:`HttpDevoTokenAuth` that authenticates a request with HTTP
    Bearer authentication scheme.
    """

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        """Adds the header ``Authorization: Bearer <token>`` to the request.

        :param req: The request object to authenticate
        :return: The request object authenticated with proper header
        """
        req.headers['Authorization'] = f"Bearer {self.token}"
        return req
