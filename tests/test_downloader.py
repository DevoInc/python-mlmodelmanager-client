import os

import pytest

from devo_ml.modelmanager import engines
from devo_ml.modelmanager.downloader import Downloader, FileSystemDownloader
from devo_ml.modelmanager.downloader import get_default_downloader
from devo_ml.modelmanager.downloader import get_image_bytes


def test_get_default_downloader():
    assert isinstance(get_default_downloader(), Downloader)


def test_file_system_downloader(encoded_image, tmp_path):
    model = {
        "name": "model_name",
        "engine": engines.IDA,
        "image": {"id": 1, "image": encoded_image, "size": 295}
    }
    output_file = FileSystemDownloader(tmp_path)(model)
    with open(output_file, "rb") as f:
        file_content = f.read()
    assert file_content == get_image_bytes(model.get("image"))
    os.remove(output_file)


def test_file_system_downloader_with_invalid_model(encoded_image, tmp_path):
    with pytest.raises(ValueError):
        FileSystemDownloader(tmp_path)({
            "engine": engines.IDA,
            "image": {"id": 1, "image": encoded_image, "size": 295}
        })
    with pytest.raises(ValueError):
        FileSystemDownloader(tmp_path)({
            "model": "model_name",
            "image": {"id": 1, "image": encoded_image, "size": 295}
        })
    with pytest.raises(ValueError):
        FileSystemDownloader(tmp_path)({
            "model": "model_name",
            "engine": engines.IDA,
            "image": {"id": 1, "size": 295}
        })


def test_file_system_downloader_set_absolute_path():
    downloader = FileSystemDownloader("foo")
    assert os.path.isabs(downloader.path)
