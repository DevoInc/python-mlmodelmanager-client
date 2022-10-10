from __future__ import annotations

from typing import Optional

from .auth import AuthCallable
from .api import Api
from .downloader import DownloaderCallable, get_default_downloader
from .endpoint import EndpointRenderer, LegacyEndpointRenderer
from .error import ModelManagerError, ModelNotFound, ModelAlreadyExists
from .validator import is_valid_url


class Client:
    def __init__(
        self,
        url: str,
        auth: AuthCallable = None,
        downloader: DownloaderCallable = None,
        **kwargs
    ):
        if not is_valid_url(url):
            raise ModelManagerError(msg=f"Invalid url: '{url}'")
        self.endpoints = EndpointRenderer(url)
        self.api = Api(auth=auth, **kwargs)
        self.downloader = downloader or get_default_downloader()

    @property
    def url(self):
        return self.endpoints.url

    def get_models(self) -> list[dict]:
        endpoint = self.endpoints.models()
        return self.api.get(endpoint)

    def get_model(self, name: str, download_file: bool = None) -> dict:
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
        self, name: str,
        download_file: bool = None
    ) -> Optional[dict]:
        try:
            return self.get_model(name, download_file=download_file)
        except ModelNotFound:
            return None

    def add_model(
        self,
        name: str,
        engine: str,
        upload_path: str,
        description: str = None,
        force: bool = None
    ) -> dict:
        model = self.api.get(self.endpoints.model(name), params={"fast": True})
        if model and not force:
            raise ModelAlreadyExists(name)
        image_metadata = self.api.post(
            self.endpoints.image_upload(),
            data={"engine": engine},
            files=[('fileName', open(upload_path, 'rb'))]
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
        self.api.post(self.endpoints.models(), json=body)
        return image_metadata


class LegacyClient(Client):
    def __init__(self, url: str, domain: str, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.endpoints = LegacyEndpointRenderer(url, domain)
