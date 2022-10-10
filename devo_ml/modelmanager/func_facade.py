from __future__ import annotations

from typing import Optional

from .auth import create_auth_from_token, STANDALONE
from .client import Client
from .downloader import FileSystemDownloader as DefaultDownloader


def get_models(
    url: str,
    token: str,
    auth_type: str = STANDALONE,
    **kwargs
) -> list[dict]:
    auth = create_auth_from_token(token, auth_type=auth_type)
    return Client(url, auth=auth, **kwargs).get_models()


def get_model(
    url: str,
    token: str,
    name: str,
    auth_type: str = STANDALONE,
    download_path: str = None,
    **kwargs
) -> dict:
    auth = create_auth_from_token(token, auth_type=auth_type)
    downloader = DefaultDownloader(download_path) if download_path else None
    client = Client(url, auth=auth, downloader=downloader, **kwargs)
    return client.get_model(name, download_file=bool(download_path))


def find_model(
    url: str,
    token: str,
    name: str,
    auth_type: str = STANDALONE,
    download_path: str = None,
    **kwargs
) -> Optional[dict]:
    auth = create_auth_from_token(token, auth_type=auth_type)
    downloader = DefaultDownloader(download_path) if download_path else None
    client = Client(url, auth=auth, downloader=downloader, **kwargs)
    return client.find_model(name, download_file=bool(download_path))


def add_model(
    url: str,
    token: str,
    name: str,
    engine: str,
    upload_path: str,
    description: str = None,
    auth_type: str = STANDALONE,
    force: bool = None,
    **kwargs
) -> dict:
    auth = create_auth_from_token(token, auth_type=auth_type)
    client = Client(url, auth=auth, **kwargs)
    return client.add_model(
        name,
        engine,
        upload_path,
        description=description,
        force=force
    )
