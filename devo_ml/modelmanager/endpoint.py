from __future__ import annotations

from urllib.parse import quote


class EndpointRenderer:
    def __init__(self, url: str) -> None:
        self.url = url.rstrip('/')

    def models(self) -> str:
        return f"{self.url}/models"

    def model(self, name: str) -> str:
        return f"{self.url}/models/{quote(name)}"

    def image_upload(self) -> str:
        return f"{self.url}/models/images/upload"


class LegacyEndpointRenderer(EndpointRenderer):
    def __init__(self, url: str, domain: str) -> None:
        super().__init__(url)
        self.domain = domain

    def models(self) -> str:
        return f"{self.url}/domains/{self.domain}/models"

    def model(self, name: str) -> str:
        return f"{self.url}/domains/{self.domain}/models/{quote(name)}"

    def image_upload(self) -> str:
        return f"{self.url}/domains/{self.domain}/models/images/upload"
