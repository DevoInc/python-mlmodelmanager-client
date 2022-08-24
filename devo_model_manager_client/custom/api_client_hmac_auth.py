import hashlib
import hmac
import json
import time

from devo_model_manager_client import ApiClient


class ApiClientHMACAuth(ApiClient):
    """
    Custom client with DEVO HMAC authentication.
    The DEVO api key based authentication is special because it uses HMAC to sign the request
    contents with a secret (the api secret)
    This authentication method is not support by swagger codegen so we have to override the default ApiClient
    class to add support for it.
    """

    def __init__(self, api_key, api_secret, *args, **kwargs):
        self.api_key = api_key
        self.api_secret = api_secret
        super(ApiClientHMACAuth, self).__init__(*args, **kwargs)

    def call_api(self, resource_path, method, path_params=None, query_params=None, header_params=None, body=None,
                 post_params=None, files=None, response_type=None, auth_settings=None, async_req=None,
                 _return_http_data_only=None, collection_formats=None, _preload_content=True, _request_timeout=None):
        # Setup HMAC headers
        timestamp_millis = str(int(round(time.time() * 1000)))

        if body is None:
            body_to_sign = bytearray('', 'UTF-8')
        else:
            if isinstance(body, str):
                body_to_sign = bytearray(body, 'UTF-8')
            else:
                sanitized = super(ApiClientHMACAuth, self).sanitize_for_serialization(body)
                body_to_sign = bytearray(json.dumps(sanitized), 'UTF-8')

        header_params['x-logtrust-timestamp'] = timestamp_millis
        header_params['x-logtrust-domain-apikey'] = self.api_key
        header_params['x-logtrust-sign'] = \
            hmac.new(
                bytearray(self.api_secret, 'UTF-8'),
                bytearray(self.api_key, 'UTF-8') + body_to_sign + bytearray(timestamp_millis, 'UTF-8'),
                hashlib.sha256).hexdigest()

        return super(ApiClientHMACAuth, self) \
            .call_api(resource_path, method, path_params, query_params, header_params, body, post_params,
                      files, response_type, auth_settings, async_req, _return_http_data_only,
                      collection_formats, _preload_content, _request_timeout)
