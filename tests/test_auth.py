import pytest

from devo_ml.modelmanager import auth


@pytest.mark.parametrize("auth_class,token,header_key,payload", [
    (
        auth.HttpDevoStandAloneTokenAuth,
        "myToken", "standAloneToken", "myToken"
    ),
    (
        auth.HttpDevoBearerTokenAuth,
        "myToken", "Authorization", "Bearer myToken"
    ),
])
def test_authorize_request_with_token(
    auth_class,
    token,
    header_key,
    payload,
    get_request
):
    authentication = auth_class(token)
    request = authentication(get_request({"foo": "bar", "baz": "quz"}))
    assert request.headers.get(header_key) == payload
