from __future__ import annotations

import base64
import os

from pathlib import Path
from typing import Callable

from .engines import get_default_engine_extension


DownloaderCallable = Callable[[dict], str]


def get_default_downloader() -> Downloader:
    """Returns the default downloader used.

    :return: The default downloader
    :rtype: Downloader
    """
    return FileSystemDownloader(".")


def get_image_bytes(image: dict) -> bytes:
    """Get the bytes of an image.

    An image must have the `image` key with the base 64 encoded image.

    :param image: The image to get bytes
    :type image: dict
    :raises: ValueError: if no image key or image key is empty.
    :return: The bytes of the image
    :rtype: bytes
    """
    encoded_image = image.get("image")
    if not encoded_image:
        raise ValueError("Invalid image")
    return base64.b64decode(encoded_image)


class Downloader:
    """An interface to downloaders.

    Any downloader must be a callable with the `DownloaderCallable` signature,
    receiving a model and returns an identification of the download of the
    model as a string.
    """

    def __call__(self, model: dict) -> str:
        raise NotImplementedError("Downloader must be callable.")


class FileSystemDownloader(Downloader):
    """A downloader capable of writing file of model to the file system.

    :param path: The path where files will be written
    :type path: str | Path
    """

    def __init__(self, path: str | Path) -> None:
        self.path = os.path.abspath(os.path.expanduser(path))

    def __call__(self, model: dict) -> str:
        """Downloads the file associated with the model and writes it
        in downloader path.

        The file name will be the model name plus the inferred extension from
        the engine. The extension will be empty if it can not infer, e.g: if
        there is no extension associated to the engine.

        :param model: The model to download its file
        :type model: dict
        :raises: ValueError: If model has invalid or empty keys for `name`,
            `engine` or `image`
        :raises: OSError: If there is a problem writing the file to path
        :return: The absolute path of file written
        :rtype: str
        """
        name = model.get("name")
        engine = model.get("engine")
        if not name or not engine:
            raise ValueError("Invalid model")
        image_bytes = get_image_bytes(model.get("image", {}))
        ext = get_default_engine_extension(engine)
        file = os.path.join(self.path, f"{name}{ext}")
        with open(file, "wb") as f:
            f.write(image_bytes)
        return file
