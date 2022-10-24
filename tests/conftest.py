import os

import pytest
import requests

from devo_ml.modelmanager.auth import create_auth_from_token, STANDALONE
from devo_ml.modelmanager.client import Client, LegacyClient
from devo_ml.modelmanager.downloader import Downloader


class MockDownloader(Downloader):
    def __call__(self, model: dict) -> str:
        return f"{self.__class__.__name__}__returns"


@pytest.fixture
def get_client():
    def _get_client(url, auth, downloader):
        return Client(url, auth, downloader=downloader)
    return _get_client


@pytest.fixture
def client(get_client):
    token = "8a3vf98ai28sar1234lkj2l43td6f89a"
    return get_client(
        "http://localhost",
        create_auth_from_token(token, auth_type=STANDALONE),
        downloader=MockDownloader()
    )


@pytest.fixture
def get_legacy_client():
    def _get_legacy_client(url, domain, auth, downloader):
        return LegacyClient(url, domain, auth, downloader=downloader)
    return _get_legacy_client


@pytest.fixture
def legacy_client(get_legacy_client):
    token = "8a3vf98ai28sar1234lkj2l43td6f89a"
    return get_legacy_client(
        "http://localhost",
        "self",
        create_auth_from_token(token, auth_type=STANDALONE),
        downloader=MockDownloader()
    )


@pytest.fixture
def get_request():
    def _get_request(data):
        req = requests.Request()
        req.url = "http://localhost"
        req.data = data
        return req.prepare()
    return _get_request


@pytest.fixture
def encoded_image():
    return (
        "ewogICJtZXRhZGF0YSIgOiB7CiAgICAiaWQiOiAxMjM0NTYsCiAgICAibmFtZSI6ICJod"
        "W1hbl91c2FibGVfc2F2ZWRfbmFtZSIsCiAgICAiYWxnb3JpdGhtIjogImhvbHR3aW50ZX"
        "JzIiwKICAgICJ2ZXJzaW9uIjogIjEuMCIKICB9LAogICJkYXRhIiA6IHsKICAgICJhbHB"
        "oYSIgOiAwLjUsCiAgICAiYmV0YSIgOiAwLjUsCiAgICAiZ2FtbWEiIDogMC41LAogICAg"
        "InNlYXNvbkxlbmd0aCIgOiAxMCwKICAgICJzZWFzb25hbE1ldGhvZCIgOiAiYWRkaXRpd"
        "mUiLAogICAgInRyYWluaW5nUGVyaW9kcyIgOiAzCiAgfQp9Cg=="
    )


@pytest.fixture
def image_metadata():
    return {
        "valid": True,
        "errorDetail": None,
        "outputType": "str",
        "category": "Binomial",
        "imageId": 1,
        "fields": [
            {
                "id": None,
                "name": "Pclass",
                "description": "",
                "type": "str"
            },
            {
                "id": None,
                "name": "Sex",
                "description": "",
                "type": "str"
            },
            {
                "id": None,
                "name": "Age",
                "description": "",
                "type": "float8"
            },
            {
                "id": None,
                "name": "SibSp",
                "description": "",
                "type": "float8"
            },
            {
                "id": None,
                "name": "Parch",
                "description": "",
                "type": "float8"
            },
            {
                "id": None,
                "name": "Fare",
                "description": "",
                "type": "float8"
            },
            {
                "id": None,
                "name": "Cabin",
                "description": "",
                "type": "str"
            },
            {
                "id": None,
                "name": "Embarked",
                "description": "",
                "type": "str"
            }
        ],
        "clusters": [],
        "fileName": "test.zip",
        "size": 240406,
        "runtimeSize": 268124
    }


@pytest.fixture
def abs_path():
    def _abs_path(file_name=""):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            file_name
        )
    return _abs_path


@pytest.fixture
def mock_get_models(requests_mock):
    def _mock_get_models(code=None, response=None):
        url = "http://localhost/models"
        requests_mock.get(url, status_code=code or 200, json=response)
    return _mock_get_models


@pytest.fixture
def mock_get_model(requests_mock):
    def _mock_get_model(name, fast=True, code=None, response=None):
        url = f"http://localhost/models/{name}?fast={bool(fast)}"
        requests_mock.get(url, status_code=code or 200, json=response)
    return _mock_get_model


@pytest.fixture
def mock_post_model(requests_mock):
    def _mock_post_model(code=None, response=None):
        requests_mock.post(
            "http://localhost/models",
            status_code=code or 200,
            json=response
        )
    return _mock_post_model


@pytest.fixture
def mock_image_upload(requests_mock):
    def _mock_image_upload(code=None, response=None):
        requests_mock.post(
            "http://localhost/models/images/upload",
            status_code=code or 200,
            json=response
        )
    return _mock_image_upload
