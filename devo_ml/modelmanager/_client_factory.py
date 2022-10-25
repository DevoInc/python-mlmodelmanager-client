from .auth import create_auth_from_token, get_default_auth_type
from ._client import Client
from .downloader import FileSystemDownloader
from .profile import read_profile_from_file


def create_client_from_token(
    url: str,
    token: str,
    auth_type: str = None,
    download_path: str = None,
    **kwargs
) -> Client:
    """Creates an ML Model Manager
    :class:`Client <devo_ml.modelmanager.client.Client>` with token
    authentication.

    :param url: The URL of the server
    :param token: The token to authenticate
    :param auth_type: The type of authentication to use;
        :const:`STANDALONE <devo_ml.modelmanager.auth.STANDALONE>` or
        :const:`BEARER <devo_ml.manager.auth.BEARER>`.
        :func:`get_default_auth_type()
        <devo_ml.manager.auth.get_default_auth_type>`
        is used if is not provided
    :param download_path: The path where model files will be downloaded. The
        current directory ``.`` is used if not provided.
    :param kwargs: Additional options for underlying request, e.g. `timeout`.
        These options are the same of the ``requests`` library can manage
    :return: A ready to use Client object
    """
    auth_type = auth_type or get_default_auth_type()
    auth = create_auth_from_token(token, auth_type=auth_type)
    downloader = FileSystemDownloader(download_path) if download_path else None
    return Client(url, auth, downloader=downloader, **kwargs)


def create_client_from_profile(
    profile: str,
    path: str = None,
    **kwargs
) -> Client:
    """Creates an ML Model Manager
    :class:`Client <devo_ml.modelmanager.client.Client>` from a profile located
    in a file.

    The profile file is an `INI` file with this shape:

    .. code-block:: ini

        [dev]
        url = https://dev_url
        token = 8a3vf98ai28sar1234lkj2l43td6f89a
        auth_type = standalone
        download_path = ~/models

    :param profile: The name of the profile to use
    :param path: The path, file path or filename to search for a profile
    :param kwargs: Additional options for underlying request, e.g. `timeout`.
        These options are the same of the
        :doc:`Requests <requests:user/quickstart>` library can manage
    :return: A ready to use Client object
    """
    cfg = read_profile_from_file(profile, path=path)
    return create_client_from_token(
        cfg["url"],
        cfg["token"],
        auth_type=cfg["auth_type"],
        download_path=cfg["download_path"],
        **kwargs
    )
