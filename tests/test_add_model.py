import pytest

from devo_ml.modelmanager import engines
from devo_ml.modelmanager.error import ModelManagerError, ModelAlreadyExists


def test_add_non_existing_model(
    client,
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model,
    image_metadata
):
    mock_get_model("model_name", fast=True)
    mock_image_upload(response=image_metadata)
    mock_post_model()
    response = client.add_model(
        "model_name",
        engines.IDA,
        abs_path("./data/test.zip")
    )
    assert response == image_metadata


def test_add_existing_model_without_force(client, abs_path, mock_get_model):
    mock_get_model("model_name", fast=True, response={"name": "model_name"})
    with pytest.raises(ModelAlreadyExists):
        client.add_model(
            "model_name",
            engines.IDA,
            abs_path("./data/test.zip")
        )


def test_add_existing_model_with_force(
    client,
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model,
    image_metadata
):
    name = "model_name"
    mock_get_model(name, fast=True, response={"id": "1", "name": name})
    mock_image_upload(response=image_metadata)
    mock_post_model()
    response = client.add_model(
        name,
        engines.IDA,
        abs_path("./data/test.zip"),
        force=True
    )
    assert response == image_metadata


def test_add_model_with_invalid_engine(
    client,
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
    with pytest.raises(ModelManagerError) as e:
        client.add_model(
            "model_name",
            "INVALID_ENGINE",
            abs_path("./data/test.zip")
        )
    assert e.value.code == 500
    assert "INVALID_ENGINE" in str(e.value)


def test_add_model_with_invalid_image(
    client,
    abs_path,
    mock_get_model,
    mock_image_upload,
    mock_post_model
):
    mock_get_model("model_name", fast=True)
    mock_image_upload(
        response={"valid": False, "errorDetail": "Invalid image"}
    )
    mock_post_model()
    with pytest.raises(ModelManagerError):
        client.add_model(
            "model_name",
            engines.IDA,
            abs_path("./data/test.zip")
        )
