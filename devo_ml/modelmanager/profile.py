import configparser
import os

from typing import Any

from .auth import validate_auth_type, get_default_auth_type
from .error import ProfileError, ProfileValueRequired
from .validator import is_valid_url


def read_profile_from_file(profile: str, path: str = None) -> dict:
    try:
        profile_file = resolve_profile_file(path=path)
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(profile_file))
        if profile not in config:
            raise ProfileError(f"Missing profile '{profile}'")
        values = config[profile]
        url = get_required_profile_value(values, "url")
        if not is_valid_url(url):
            raise ProfileError(f"Invalid url: '{url}'")
        token = get_required_profile_value(values, "token")
        auth_type = values.get("auth_type", get_default_auth_type())
        if not validate_auth_type(auth_type):
            raise ProfileError(f"Invalid auth type '{auth_type}'")
        return {
            "url": url,
            "token": token,
            "auth_type": auth_type,
            "download_path": values.get("download_path"),
        }
    except configparser.Error as e:
        raise ProfileError(str(e)) from e


def get_required_profile_value(
    section: configparser.SectionProxy,
    key: str
) -> Any:
    value = section.get(key)
    if not value:
        raise ProfileValueRequired(key)
    return value


def resolve_profile_file(path: str = None, file_name: str = None) -> str:
    file_name = file_name or "modelmanager.ini"
    resolver_order = [".", os.path.expanduser("~")]
    if path and path not in resolver_order:
        resolver_order.insert(0, path)
    for resolve_path in resolver_order:
        if os.path.isfile(resolve_path):
            return resolve_path
        f = os.path.join(resolve_path, file_name)
        if os.path.isfile(f):
            return f
    raise ProfileError(f"File not found in resolver order: {resolver_order}")
