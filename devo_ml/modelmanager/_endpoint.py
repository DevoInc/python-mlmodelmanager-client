from __future__ import annotations

import abc

from urllib.parse import quote

from .error import ModelManagerError
from .validator import is_valid_url


class EndpointRenderer(abc.ABC):
    """An interface to endpoint renderers."""

    def __init__(self, url: str) -> None:
        """Creates an instance of this endpoint renderer.

        :param url: The URL of the ML Model Manager server
        """
        if not is_valid_url(url):
            raise ModelManagerError(msg=f"Invalid url: '{url}'")
        self.url = url.rstrip('/')

    @abc.abstractmethod
    def models(self) -> str:
        """
        :return: URL of the get models endpoint
        """

    @abc.abstractmethod
    def model(self, name: str) -> str:
        """
        :param name: The model name
        :return: URL of the get model endpoint
        """

    @abc.abstractmethod
    def image_upload(self) -> str:
        """
        :return: URL of the image upload endpoint
        """


class LatestEndpointRenderer(EndpointRenderer):
    """An :class:`EndpointRenderer` for ML Model Manager server ``2.4.0``
    and above.
    """

    def models(self) -> str:
        """Render endpoint ``<url>/models``.

        :return: URL of the get models endpoint
        """
        return f"{self.url}/models"

    def model(self, name: str) -> str:
        """Render endpoint ``<url>/models/{name}``.

        :param name: The model name
        :return: URL of the get model endpoint
        """
        return f"{self.url}/models/{quote(name)}"

    def image_upload(self) -> str:
        """Render endpoint ``<url>/models/images/upload``.

        :return: URL of the image upload endpoint
        """
        return f"{self.url}/models/images/upload"


class LegacyEndpointRenderer(EndpointRenderer):
    """A :class:`EndpointRenderer` for ML Model Manager server prior to
    ``2.4.0``."""

    def __init__(self, url: str, domain: str) -> None:
        """Creates an instance of this endpoint renderer.

        :param url: The url of the ML Model Manager server
        :param domain: The domain referrer
        """
        super().__init__(url)
        self.domain = domain

    def models(self) -> str:
        """Render endpoint ``<url>/domains/{domain}/models``.

        :return: URL of the get models endpoint
        """
        return f"{self.url}/domains/{self.domain}/models"

    def model(self, name: str) -> str:
        """Render endpoint ``<url>/domains/{domain}/models/{name}``.

        :param name: The model name
        :return: URL of the get model endpoint
        """
        return f"{self.url}/domains/{self.domain}/models/{quote(name)}"

    def image_upload(self) -> str:
        """Render endpoint ``<url>/domains/{domain}/models/images/upload``.

        :return: URL of the image upload endpoint
        """
        return f"{self.url}/domains/{self.domain}/models/images/upload"
