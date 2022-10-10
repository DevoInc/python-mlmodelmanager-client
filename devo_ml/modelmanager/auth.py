from __future__ import annotations

import requests

from typing import Callable
from requests import PreparedRequest


AuthCallable = Callable[[PreparedRequest], PreparedRequest]

BEARER = "bearer"
STANDALONE = "standalone"


def get_default_auth_type():
    return STANDALONE


def validate_auth_type(auth_type: str) -> bool:
    return auth_type in (BEARER, STANDALONE)


def create_auth_from_token(
    token: str,
    auth_type: str = STANDALONE
) -> AuthCallable:
    if not validate_auth_type(auth_type):
        raise ValueError(f"Invalid auth type: '{auth_type}'")
    return {
        BEARER: HttpDevoBearerTokenAuth,
        STANDALONE: HttpDevoStandAloneTokenAuth,
    }.get(auth_type, HttpDevoStandAloneTokenAuth)(token)


class HttpDevoTokenAuth(requests.auth.AuthBase):
    """An authentication based on a token.

    :param token: The token use by the auth
    :type token: str
    """

    def __init__(self, token: str) -> None:
        self.token = token


class HttpDevoStandAloneTokenAuth(HttpDevoTokenAuth):
    """An :class:`HttpDevoTokenAuth` based on a `standAloneToken` auth_type."""

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        req.headers['standAloneToken'] = self.token
        return req


class HttpDevoBearerTokenAuth(HttpDevoTokenAuth):
    """An :class:`HttpDevoTokenAuth` based on a `bearer` auth_type."""

    def __call__(self, req: PreparedRequest) -> PreparedRequest:
        req.headers['Authorization'] = f"Bearer {self.token}"
        return req
