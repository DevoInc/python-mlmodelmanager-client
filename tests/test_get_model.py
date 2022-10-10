import pytest

from devo_ml.modelmanager import engines
from devo_ml.modelmanager import error


def test_get_existing_model(client, mock_get_model):
    mock_get_model("name", response={"name": "name", "engine": engines.ONNX})
    response = client.get_model("name")
    assert response == {"name": "name", "engine": engines.ONNX}


def test_get_existing_model_with_download_file(
    client,
    abs_path,
    encoded_image,
    mock_get_model
):
    mock_get_model(
        "model_name",
        fast=False,
        response={
            "name": "model_name",
            "engine": engines.IDA,
            "image": {"id": 1, "image": encoded_image, "size": 295}
        }
    )
    model = client.get_model("model_name", download_file=True)
    assert model == {
        "name": "model_name",
        "engine": engines.IDA,
        "file": "MockDownloader__returns"
    }


def test_get_non_existing_model(client, mock_get_model):
    mock_get_model("model_name", code=204)
    with pytest.raises(error.ModelNotFound):
        client.get_model("model_name")


def test_get_model_with_empty_model_name(client, mock_get_model):
    mock_get_model("")
    with pytest.raises(error.ModelManagerError):
        client.get_model("")


def test_get_model_with_invalid_token(client, mock_get_model):
    mock_get_model(
        "model_name",
        code=403,
        response={
            "code": 5,
            "msg": "Token invalid or expired",
            "cid": "123"
        }
    )
    with pytest.raises(error.TokenError):
        client.get_model("model_name")
