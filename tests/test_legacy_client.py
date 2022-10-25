import pytest

from devo_ml.modelmanager.error import ModelManagerError


def test_network_error(legacy_client):
    with pytest.raises(ModelManagerError):
        legacy_client.get_model("model_name")
