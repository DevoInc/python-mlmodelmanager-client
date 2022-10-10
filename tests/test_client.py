import pytest

from devo_ml.modelmanager import auth
from devo_ml.modelmanager.error import ModelManagerError
from devo_ml.modelmanager import client_factory as factory


def test_network_error(client):
    with pytest.raises(ModelManagerError):
        client.get_model("model_name")


@pytest.mark.parametrize("auth_type,auth_class", [
    (auth.BEARER, auth.HttpDevoBearerTokenAuth),
    (auth.STANDALONE, auth.HttpDevoStandAloneTokenAuth),
    (None, auth.HttpDevoStandAloneTokenAuth),
])
def test_create_client_from_token(auth_type, auth_class):
    client = factory.create_client_from_token(
        "http://localhost",
        "the_token",
        auth_type=auth_type
    )
    assert isinstance(client.api.auth, auth_class)


def test_create_client_from_token_with_invalid_url(get_client):
    with pytest.raises(ModelManagerError):
        factory.create_client_from_token("http://invalid url", "token")


def test_create_client_from_token_with_invalid_auth_type():
    with pytest.raises(ValueError):
        factory.create_client_from_token(
            "http://localhost",
            "the_token",
            auth_type="foo"
        )


def test_create_client_from_profile(abs_path):
    client = factory.create_client_from_profile(
        "testing",
        path=abs_path("./profiles/modelmanager.ini")
    )
    assert client.url == "https://localhost"
