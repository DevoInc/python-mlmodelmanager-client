from devo_ml.modelmanager.endpoint import EndpointRenderer
from devo_ml.modelmanager.endpoint import LegacyEndpointRenderer


def test_endpoint_renderer():
    endpoints = EndpointRenderer("http://localhost")
    assert endpoints.models() ==  "http://localhost/models"
    assert endpoints.model("foo") == "http://localhost/models/foo"
    assert endpoints.image_upload() == "http://localhost/models/images/upload"
    endpoints = EndpointRenderer("http://localhost/")
    assert endpoints.models() ==  "http://localhost/models"
    assert endpoints.model("foo") == "http://localhost/models/foo"
    assert endpoints.image_upload() == "http://localhost/models/images/upload"


def test_legacy_endpoint_renderer():
    endpoints = LegacyEndpointRenderer("http://localhost", "self")
    assert endpoints.models() == "http://localhost/domains/self/models"
    assert endpoints.model("foo") == "http://localhost/domains/self/models/foo"  # noqa
    assert endpoints.image_upload() == "http://localhost/domains/self/models/images/upload"  # noqa
    endpoints = LegacyEndpointRenderer("http://localhost/", "self")
    assert endpoints.models() == "http://localhost/domains/self/models"
    assert endpoints.model("foo") == "http://localhost/domains/self/models/foo"  # noqa
    assert endpoints.image_upload() == "http://localhost/domains/self/models/images/upload"  # noqa
