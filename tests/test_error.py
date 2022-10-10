import pytest


from devo_ml.modelmanager import error


def test_model_manager_error():
    e = error.ModelManagerError(code=1, msg="test_error")
    assert str(e) == "1: test_error"


@pytest.mark.parametrize("code,error_class", [
    (5, error.TokenError),
])
def test_create_model_manager_error_from_code(code, error_class):
    assert isinstance(error.ModelManagerError.from_code(code), error_class)
