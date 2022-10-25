from devo_ml.modelmanager import engines


def test_find_existing_model(client, mock_get_model):
    mock_get_model("name", response={"name": "name", "engine": engines.ONNX})
    model = client.find_model("name")
    assert model == {"name": "name", "engine": engines.ONNX}


def test_find_existing_model_with_download_file(
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


def test_find_non_existing_model(client, mock_get_model):
    mock_get_model("model_name", code=200)
    model = client.find_model("model_name")
    assert model is None
