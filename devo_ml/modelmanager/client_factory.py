from .auth import create_auth_from_token, get_default_auth_type
from .client import Client
from .downloader import FileSystemDownloader
from .profile import read_profile_from_file


def create_client_from_token(
    url: str,
    token: str,
    auth_type: str = None,
    download_path: str = None,
    **kwargs
) -> Client:
    auth_type = auth_type or get_default_auth_type()
    auth = create_auth_from_token(token, auth_type=auth_type)
    downloader = FileSystemDownloader(download_path) if download_path else None
    return Client(url, auth=auth, downloader=downloader, **kwargs)


def create_client_from_profile(
    profile: str,
    path: str = None,
    **kwargs
) -> Client:
    cfg = read_profile_from_file(profile, path=path)
    return create_client_from_token(
        cfg["url"],
        cfg["token"],
        auth_type=cfg["auth_type"],
        downaload_path=cfg["download_path"],
        **kwargs
    )
