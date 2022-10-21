"""Profile helper functions."""

from __future__ import annotations

import configparser
import os

from pathlib import Path
from typing import Any

from .auth import validate_auth_type, get_default_auth_type
from .error import ProfileError, ProfileValueRequired
from .validator import is_valid_url


def read_profile_from_file(profile: str, path: str = None) -> dict:
    """Reads the profile located in a file.

    A set of paths is built in order to search for a profile file:

        * `path` if provided.
        * current directory, ``.``.
        * user's home directory, ``/home/<user>/``.

    The file to read the profile will be the file contained in path if there is
    a file name in path, otherwise `modelmanager.ini`.

    A profile has this shape in a profile file:

        .. code-block:: ini

            [dev]
            url = https://dev_url
            token = 8a3vf98ai28sar1234lkj2l43td6f89a
            auth_type = standalone
            download_path = ~/models

    and it is parsed to this python dict:

        .. code-block::

            {
                "url": "https://dev_url",
                "token": "8a3vf98ai28sar1234lkj2l43td6f89a",
                "auth_type": "standalone",
                "download_path": "~/models",
            }

    :param profile: Name of the profile to read
    :param path: Path, file path or file name to search for a profile file
    :raises ProfileError: if no file found, or if profile not found in the
        file, or if values of the profile don't pass the validation, or any
        syntax error in the file detected
    :return: The profile values found
    """
    try:
        paths: list[str | Path] = [".", os.path.expanduser("~")]
        file = None
        path = os.path.expanduser(path or "")
        if os.path.isfile(path):
            path, file = os.path.split(path)
        if path and path not in paths:
            paths.insert(0, path)
        profile_file = resolve_profile_file(paths, file_name=file)
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
        download_path = values.get("download_path")
        if download_path:
            download_path = os.path.expanduser(download_path)
        return {
            "url": url,
            "token": token,
            "auth_type": auth_type,
            "download_path": download_path,
        }
    except configparser.Error as e:
        raise ProfileError(str(e)) from e


def get_required_profile_value(
    section: configparser.SectionProxy,
    key: str
) -> Any:
    """Gets the value of a key of a
    :doc:`ConfigParser <python:library/configparser>` object section.

    The key must exists in the section, and the value must not be empty,
    otherwise an exception will be raised.

    :param section: The config parser section to extract the value
    :param key: The target key
    :raises ProfileValueRequired: If value found is empty or key doesn't exist
    :return: The value found
    """
    value = section.get(key)
    if not value:
        raise ProfileValueRequired(key)
    return value


def resolve_profile_file(
    paths: list[str | Path],
    file_name: str = None
) -> str:
    """Searches a profile file in a list of paths.

    It searches for `file_name` if it is provided, `modelmanager.ini`
    otherwise.

    :param paths: The set of paths for searching a profile file
    :param file_name: The file to search
    :raises ProfileError: If no file found in paths set.
    :return: The file path of the profile file found
    """
    file_name = file_name or "modelmanager.ini"
    for path in paths:
        f = os.path.join(path, file_name)
        if os.path.isfile(f):
            return f
    raise ProfileError(f"File not found in paths: {paths}")
