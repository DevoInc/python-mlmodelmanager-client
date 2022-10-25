from __future__ import annotations

from typing import Optional, List

from ._client_factory import create_client_from_token


def get_models(
    url: str,
    token: str,
    auth_type: str = None,
    **kwargs
) -> List[dict]:
    """Gets the list of the models in the system.

    :param url: The URL of the server. Must be valid
    :param token: The token to authenticate
    :param auth_type: The type of the authentication,
        :func:`get_default_auth_type
        <devo_ml.modelmanager.auth.get_default_auth_type>`
        is used if it is not provided
    :param kwargs: Options to the underlying requests
    :return: The list of the models
    """
    return create_client_from_token(
        url,
        token,
        auth_type=auth_type,
        **kwargs
    ).get_models()


def get_model(
    url: str,
    token: str,
    name: str,
    auth_type: str = None,
    download_path: str = None,
    **kwargs
) -> dict:
    """Gets a model by its name.

    :param url: The URL of the server. Must be valid
    :param token: The token to authenticate
    :param name: The name of the model
    :param auth_type: The type of the authentication,
        :func:`get_default_auth_type
        <devo_ml.modelmanager.auth.get_default_auth_type>`
        is used if it is not provided
    :param download_path:
    :param kwargs: Options to the underlying requests
    :raises ModelNotFound: If the model doesn't exist
    :return: The model data
    """
    return create_client_from_token(
        url,
        token,
        auth_type=auth_type,
        download_path=download_path,
        **kwargs
    ).get_model(name, download_file=bool(download_path))


def find_model(
    url: str,
    token: str,
    name: str,
    auth_type: str = None,
    download_path: str = None,
    **kwargs
) -> Optional[dict]:
    """Finds a model by its name.

    :param url: The URL of the server. Must be valid
    :param token: The token to authenticate
    :param name: The name of the model
    :param auth_type: The type of the authentication,
        :func:`get_default_auth_type
        <devo_ml.modelmanager.auth.get_default_auth_type>`
        is used if it is not provided
    :param download_path:
    :param kwargs: Options to the underlying requests
    :return: The model data or nothing if the model doesn't exist
    """
    return create_client_from_token(
        url,
        token,
        auth_type=auth_type,
        download_path=download_path,
        **kwargs
    ).find_model(name, download_file=bool(download_path))


def add_model(
    url: str,
    token: str,
    name: str,
    engine: str,
    model_file: str,
    description: str = None,
    auth_type: str = None,
    force: bool = None,
    **kwargs
) -> None:
    """Adds a model.

    :param url: The URL of the server. Must be valid
    :param token: The token to authenticate
    :param name: The name of the model
    :param engine: The engine of the model
    :param model_file: The path of the file of the model
    :param description: The description of the model
    :param auth_type: The type of the authentication,
        :func:`get_default_auth_type
        <devo_ml.modelmanager.auth.get_default_auth_type>`
        is used if it is not provided
    :param force: Whether to override the model if already exist
    :param kwargs: Options to the underlying requests
    :raises ModelAlreadyExists: If the model already exists and not force
    """
    return create_client_from_token(
        url,
        token,
        auth_type=auth_type,
        **kwargs
    ).add_model(name, engine, model_file, description=description, force=force)
