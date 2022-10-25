"""Easy-to-use ML Model Manager interface."""

from ._client import Client, LegacyClient
from ._client_factory import create_client_from_token
from ._client_factory import create_client_from_profile
from ._func_facade import get_models, get_model, find_model, add_model


__all__ = [
    "Client",
    "LegacyClient",
    "create_client_from_token",
    "create_client_from_profile",
    "get_models",
    "get_model",
    "find_model",
    "add_model",
]
