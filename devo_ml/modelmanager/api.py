import requests

from typing import Any

from .auth import AuthCallable
from .error import ModelManagerError


valid_methods = ["get", "post", "patch", "put", "delete"]


def decode_response(response: requests.Response) -> Any:
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return None


def validate_or_raise_error(status_code: int, response: Any) -> None:
    if 200 <= status_code < 300:
        return None
    if isinstance(response, dict):
        raise ModelManagerError.from_code(
            response.get("code", 0),
            msg=response.get("msg", "Unexpected error")
        )
    raise ModelManagerError(code=0, msg="Unexpected error")


class Api:
    def __init__(self, auth: AuthCallable = None, **kwargs):
        self.auth = auth
        self.timeout = kwargs.pop("timeout", None) or 30
        self.request_options = kwargs
        self._http_method = "get"

    def __getattr__(self, attr):
        if attr not in valid_methods:
            return super().__getattr__(attr)
        self._http_method = attr
        return self

    def __call__(self, endpoint, **kwargs) -> Any:
        response = self.request(endpoint, **kwargs)
        decoded_response = decode_response(response)
        validate_or_raise_error(response.status_code, decoded_response)
        return decoded_response

    def request(self, endpoint: str, **kwargs) -> requests.Response:
        try:
            options = self.build_request_options(**kwargs)
            return requests.request(self._http_method, endpoint, **options)
        except requests.exceptions.RequestException as e:
            raise ModelManagerError(msg=str(e)) from e

    def build_request_options(self, **kwargs) -> dict:
        timeout = kwargs.pop("timeout", self.timeout)
        auth = kwargs.pop("auth", self.auth)
        options = {**self.request_options}
        options.update(auth=auth, timeout=timeout, **kwargs)
        return options
