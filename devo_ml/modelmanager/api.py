"""Low-level HTTP API Rest access in a :doc:`Requests <requests:index>`
library wrapper.
"""

from __future__ import annotations

import requests

from typing import Any

from .auth import AuthCallable
from .error import ModelManagerError


valid_methods = ["get", "post", "patch", "put", "delete"]


def decode_response(response: requests.Response) -> Any:
    """Decodes a requests response to json.

    :param response: The requests response
    :return: A decoded response or None if any decode error.
    """
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return None


def validate_or_raise_error(status_code: int, response: Any) -> None:
    """Checks whether a decoded response is valid.

    Depend on the status code value will raise an exception. Only 2xx status
    code are considered valid.

    :param status_code: The http status code of a response. Depend on its value
        will raise an exception. Only 2xx status code are considered valid.
    :param response: A decoded response. Just for give more information about
        the error when possible.
    :raises ModelManagerError: If is not a valid status code.
    :return: Nothing
    """
    if 200 <= status_code < 300:
        return None
    if isinstance(response, dict):
        raise ModelManagerError.from_code(
            response.get("code", 0),
            msg=response.get("msg", "Unexpected error")
        )
    raise ModelManagerError(code=0, msg="Unexpected error")


class Api:
    """Low level api calls based on :doc:`Requests <requests:index>` lib."""

    def __init__(self, auth: AuthCallable = None, **kwargs):
        """Creates a :class:`Api`.

        :param auth: The authentication to use
        :param kwargs: Options to the underlying requests
        """
        self.auth = auth
        self.timeout = kwargs.pop("timeout", None) or 30
        self.request_options = kwargs
        self._http_method = "get"

    def __getattr__(self, attr):
        """Saves method to call if `attr` is a valid method. Otherwise,
        built-in followed.

        :param attr: The attribute name to get
        :return: The object itself or the attribute value
        """
        if attr not in valid_methods:
            return super().__getattr__(attr)
        self._http_method = attr
        return self

    def __call__(self, endpoint: str, **kwargs) -> Any:
        """Call to an endpoint.

        :param endpoint: The endpoint to call
        :param kwargs: Custom options to the underlying requests for this call
        :return: The decoded response
        """
        response = self.request(endpoint, **kwargs)
        decoded_response = decode_response(response)
        validate_or_raise_error(response.status_code, decoded_response)
        return decoded_response

    def request(self, endpoint: str, **kwargs) -> requests.Response:
        """Wraps a requests call to catch any error in :exc:`ModelManagerError
        <devo_ml.modelmanager.error.ModelManagerError>`.

        :param endpoint: The endpoint to request
        :param kwargs: Custom options to the underlying requests for this
            request. Will be merged with the options of the :class:`Api`
            object.
        :raises ModelManagerError: if any
            :exc:`RequestException <requests.exceptions.RequestException>`.
        :return: Request response
        """
        try:
            options = self.build_request_options(**kwargs)
            return requests.request(self._http_method, endpoint, **options)
        except requests.exceptions.RequestException as e:
            raise ModelManagerError(msg=str(e)) from e

    def build_request_options(self, **kwargs) -> dict:
        """Builds the options for a request by merging the :class:`Api` object
        request options with the options provided.

        The options provided take precedence over the options in the
        :class:`Api` object.

        :param kwargs: Custom request options
        :return: Merged request options
        """
        timeout = kwargs.pop("timeout", self.timeout)
        auth = kwargs.pop("auth", self.auth)
        options = {**self.request_options}
        options.update(auth=auth, timeout=timeout, **kwargs)
        return options
