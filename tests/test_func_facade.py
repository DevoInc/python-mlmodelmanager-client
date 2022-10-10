import pytest
import base64
import os

from devo_ml.modelmanager import engines
from devo_ml.modelmanager import error
from devo_ml.modelmanager import get_model, find_model, add_model


@pytest.mark.parametrize("func", [get_model, find_model])
def test_get_or_find_existing_model(func, mock_get_model):
    mock_get_model("name", response={"name": "name", "engine": engines.ONNX})
    response = func("http://localhost", "token", "name")
    assert response == {"name": "name", "engine": engines.ONNX}


@pytest.mark.parametrize("func", [get_model, find_model])
def test_get_or_find_existing_model_with_download_path(
    func,
    abs_path,
    encoded_image,
    mock_get_model
):
    name = "model_name"
    mock_get_model(
        name,
        fast=False,
        response={
            "name": name,
            "engine": engines.IDA,
            "image": {"id": 1, "image": encoded_image, "size": 295}
        }
    )
    model = func(
        "http://localhost",
        "token",
        name,
        download_path=abs_path("data")
    )
    ext = engines.get_default_engine_extension(engines.IDA)
    output_file = abs_path(f"data/{name}{ext}")
    assert model == {"name": name, "engine": engines.IDA, "file": output_file}
    with open(output_file, "rb") as f:
        file_content = f.read()
    assert file_content == base64.b64decode(encoded_image)
    os.remove(output_file)


def test_get_non_existing_model(mock_get_model):
    mock_get_model("model_name", code=204)
    with pytest.raises(error.ModelNotFound):
        get_model("http://localhost", "token", "model_name")


def test_get_or_find_non_existing_model(mock_get_model):
    mock_get_model("model_name", code=204)
    model = find_model("http://localhost", "token", "model_name")
    assert model is None


@pytest.mark.parametrize("func", [get_model, find_model])
def test_get_or_find_model_with_empty_model_name(func, mock_get_model):
    mock_get_model("")
    with pytest.raises(error.ModelManagerError):
        func("http://localhost", "token", "")


@pytest.mark.parametrize("func", [get_model, find_model])
def test_get_or_find_model_with_invalid_token(func, mock_get_model):
    name = "model_name"
    mock_get_model(
        name,
        code=403,
        response={
            "code": 5,
            "msg": "Token invalid or expired",
            "cid": "123"
        }
    )
    with pytest.raises(error.TokenError):
        func("http://localhost", "token", name)


@pytest.mark.parametrize("func", [get_model, find_model])
def test_get_or_find_model_with_invalid_url(func):
    with pytest.raises(error.ModelManagerError):
        func("http://invalid url", "token", "model_name")


def test_add_non_existing_model(
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model,
    image_metadata
):
    name = "model_name"
    mock_get_model(name, fast=True)
    mock_image_upload(response=image_metadata)
    mock_post_model()
    response = add_model(
        "http://localhost",
        "token",
        name,
        engines.IDA,
        abs_path("data/test.zip")
    )
    assert response == image_metadata


def test_add_existing_model_without_force(abs_path, mock_get_model):
    mock_get_model("model_name", fast=True, response={"name": "model_name"})
    with pytest.raises(error.ModelAlreadyExists):
        add_model(
            "http://localhost",
            "token",
            "model_name",
            engines.IDA,
            abs_path("data/test.zip")
        )


def test_add_existing_model_with_force(
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model,
    image_metadata
):
    name = "model_name"
    mock_get_model(
        name,
        fast=True,
        response={"id": "1", "name": name}
    )
    mock_image_upload(response=image_metadata)
    mock_post_model()
    response = add_model(
        "http://localhost",
        "token",
        name,
        engines.IDA,
        abs_path("data/test.zip"),
        force=True
    )
    assert response == image_metadata


def test_add_model_with_invalid_engine(
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model
):
    mock_get_model("model_name", fast=True, code=204)
    mock_image_upload(
        code=500,
        response={
            "code": 500,
            "msg": "No enum constant com.devo.mlx.malevolo.common.enums.EngineType.INVALID_ENGINE",  # noqa
            "cid": "cid"
        }
    )
    mock_post_model()
    with pytest.raises(error.ModelManagerError) as e:
        add_model(
            "http://localhost",
            "token",
            "model_name",
            "INVALID_ENGINE",
            abs_path("data/test.zip")
        )
    assert e.value.code == 500
    assert "INVALID_ENGINE" in str(e.value)


def test_add_model_with_invalid_image(
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model
):
    name = "model_name"
    mock_get_model(name, fast=True)
    mock_image_upload(
        response={"valid": False, "errorDetail": "Invalid image"}
    )
    mock_post_model()
    with pytest.raises(error.ModelManagerError):
        add_model(
            "http://localhost",
            "token",
            name,
            engines.IDA,
            abs_path("data/test.zip")
        )
