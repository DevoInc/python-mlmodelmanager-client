from __future__ import annotations

import os

from typing import Optional, List

from .auth import AuthCallable
from .api import Api
from .downloader import DownloaderCallable, get_default_downloader
from ._endpoint import EndpointRenderer
from ._endpoint import LatestEndpointRenderer, LegacyEndpointRenderer
from .error import ModelManagerError, ModelNotFound, ModelAlreadyExists


class BaseClient:
    """Base class for ML Model Manager clients."""

    def __init__(
        self,
        auth: AuthCallable,
        endpoints_renderer: EndpointRenderer,
        *,
        downloader: DownloaderCallable = None,
        **kwargs
    ) -> None:
        """Creates a :class:`BaseClient`.

        :param auth: The authentication to use
        :param endpoints_renderer: How to render endpoints
        :param downloader: The downloader to use
        :param kwargs: Options to the underlying requests
        """
        self.endpoints = endpoints_renderer
        self.api = Api(auth=auth, **kwargs)
        self.downloader = downloader or get_default_downloader()

    @property
    def url(self) -> str:
        """The URL of the ML Model Manager server.

        :return: URL of the ML Model Manager server
        """
        return self.endpoints.url

    def get_models(self) -> List[dict]:
        """Gets the list of the models in the system.

        :return: The list of the models
        """
        return self.api.get(self.endpoints.models())

    def get_model(self, name: str, download_file: bool = None) -> dict:
        """Gets a model by its name.

        :param name: The name of the model
        :param download_file: Whether to download the model file
        :raises ModelNotFound: If the model doesn't exist
        :return: The model data
        """
        if not name:
            raise ModelManagerError(msg=f"Invalid name: '{name}'")
        endpoint = self.endpoints.model(name)
        model = self.api.get(endpoint, params={"fast": not download_file})
        if not model:
            raise ModelNotFound(name)
        if download_file:
            model["file"] = self.downloader(model)
        model.pop("image", None)
        return model

    def find_model(
        self,
        name: str,
        download_file: bool = None
    ) -> Optional[dict]:
        """Finds a model by its name.

        :param name: The name of the model
        :param download_file: Whether to download the model file
        :return: The model data or nothing if the model doesn't exist
        """
        try:
            return self.get_model(name, download_file=download_file)
        except ModelNotFound:
            return None

    def add_model(
        self,
        name: str,
        engine: str,
        model_file: str,
        description: str = None,
        force: bool = None
    ) -> None:
        """Adds a model.

        :param name: The name of the models
        :param engine: The engine of the model
        :param model_file: The path of the file of the model
        :param description: The description of the model
        :param force: Whether to override the model if already exist
        :raises ModelAlreadyExists: If the model already exists and not force
        """
        model = self.api.get(self.endpoints.model(name), params={"fast": True})
        if model and not force:
            raise ModelAlreadyExists(name)
        model_file = os.path.expanduser(model_file)
        image_metadata = self.api.post(
            self.endpoints.image_upload(),
            data={"engine": engine},
            files=[('fileName', open(model_file, 'rb'))]
        )
        if not image_metadata.get("valid"):
            msg = str(image_metadata.get("errorDetail", ""))
            raise ModelManagerError(msg=msg)
        body = {
            "name": name,
            "engine": engine,
            "description": description,
            "image": {
                "id": image_metadata.get("imageId"),
                "size": image_metadata.get("size")
            },
            "outputType": image_metadata.get("outputType"),
            "fields": image_metadata.get("fields"),
            "clusters": image_metadata.get("clusters"),
            "category": image_metadata.get("category"),
            "runtimeSize": image_metadata.get("runtimeSize"),
            "hidden": False
        }
        if model:
            body["id"] = model.get("id")
            if description is None:
                body["description"] = model.get("description")
        self.api.post(self.endpoints.models(), json=body)


class Client(BaseClient):
    """A client for ML Model Manager server ``2.4.0`` and above."""

    def __init__(
        self,
        url: str,
        auth: AuthCallable,
        *,
        downloader: DownloaderCallable = None,
        **kwargs
    ) -> None:
        """Creates a :class:`Client`.

        :param url: The URL of the server. Must be valid
        :param auth: The authentication to use
        :param downloader: The downloader to use
        :param kwargs: Options to the underlying requests
        """
        super().__init__(
            auth,
            LatestEndpointRenderer(url),
            downloader=downloader,
            **kwargs
        )


class LegacyClient(BaseClient):
    """A client for ML Model Manager server prior to ``2.4.0``."""

    def __init__(
        self,
        url: str,
        domain: str,
        auth: AuthCallable,
        *,
        downloader: DownloaderCallable = None,
        **kwargs
    ) -> None:
        """Creates a :class:`LegacyClient`.

        :param url: The URL of the server
        :param domain: The domain to connect to
        :param kwargs: Options to the underlying requests
        """
        super().__init__(
            auth,
            LegacyEndpointRenderer(url, domain),
            downloader=downloader,
            **kwargs
        )
