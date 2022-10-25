"""Engine code literals to identify the ML engines and infer their model
file extensions.
"""

from typing import Sequence


#: | Constant denoting `Open Neural Network Exchange <https://onnx.ai/>`_
# model.
#: | Extensions: ``.onnx``
ONNX = "ONNX"

#: | Constant denoting `H2O <https://h2o.ai/>`_ model.
#: | Extensions: ``.zip``
H2O = "H2O"

#: | Constant denoting `BigML <https://bigml.com/>`_ model.
#: | Extensions: ``.json``
BIGML = "BIGML"

#: | Constant denoting `DL4J <https://deeplearning4j.konduit.ai/>`_ model.
#: | Extensions: ``.h5``
DL4J = "DL4J"

#: | Constant denoting `CatBoost <https://catboost.ai/>`_ model.
#: | Extensions: ``.cmb``
CATBOOST = "CATBOOST"

#: | Constant denoting DeepLog CORE model.
#: | Extensions: ``.zip``
DEEPLOGCORE = "DEEPLOGCORE"

#: | Constant denoting DEEPLOG APP model.
#: | Extensions: ``.zip``
DEEPLOGAPP = "DEEPLOGAPP"

#: | Constant denoting Decision Tree model.
#: | Extensions: ``.zip``
DT = "DT"

#: | Constant denoting Iterated Distillation and Amplification model.
#: | Extensions: ``.zip``
IDA = "IDA"

#: | Constant denoting ML STATS model.
#: | Extensions: ``-``
MLSTATS = "MLSTATS"

#: | Constant denoting MUA model.
#: | Extensions: ``.zip``
MUA = "MUA"

#: | Constant denoting UNICODE model.
#: | Extensions: ``.zip``
UNICODE = "UNICODE"

#: | Constant denoting WORKFLOWS model.
#: | Extensions: ``.json``
WORKFLOWS = "WORKFLOWS"

_dot_json = ".json"
_dot_zip = ".zip"
_dot_onnx = ".onnx"
_dot_h5 = ".h5"
_dot_cbm = ".cmb"

_aware_engines = {
    ONNX: {
        "code": ONNX,
        "extensions": [_dot_onnx],
    },
    H2O: {
        "code": H2O,
        "extensions": [_dot_zip],
    },
    BIGML: {
        "code": BIGML,
        "extensions": [_dot_json],
    },
    DL4J: {
        "code": DL4J,
        "extensions": [_dot_h5],
    },
    CATBOOST: {
        "code": CATBOOST,
        "extensions": [_dot_cbm],
    },
    DEEPLOGCORE: {
        "code": DEEPLOGCORE,
        "extensions": [_dot_zip],
    },
    DEEPLOGAPP: {
        "code": DEEPLOGAPP,
        "extensions": [_dot_zip],
    },
    DT: {
        "code": DT,
        "extensions": [_dot_json],
    },
    IDA: {
        "code": IDA,
        "extensions": [_dot_json],
    },
    MLSTATS: {
        "code": MLSTATS,
        "extensions": [],
    },
    MUA: {
        "code": MUA,
        "extensions": [_dot_zip],
    },
    UNICODE: {
        "code": UNICODE,
        "extensions": [_dot_zip],
    },
    WORKFLOWS: {
        "code": WORKFLOWS,
        "extensions": [_dot_json],
    },
}


def get_engine_extensions(engine_code: str) -> Sequence[str]:
    """Returns file extensions associated with an engine represented
    by its code.

    An empty list will be returned if it is an unknown engine code.

    :param engine_code: The code of the engine
    :return: The file extensions or an empty list. Extensions include the dot,
        e.g. ``.json``, ``.zip`` ...
    """
    engine = _aware_engines.get(engine_code.upper())
    return engine.get("extensions", []) if engine else []


def get_default_engine_extension(engine_code: str) -> str:
    """Returns the file extension associated with an engine represented
    by its code.

    An empty string will be returned if it is an unknown engine code.

    :param engine_code: The code of the engine
    :return: The extension associate with an engine or empty string. Extensions
        include the dot, e.g. ``.json``, ``.zip`` ...
    """
    extensions = get_engine_extensions(engine_code)
    return extensions[0] if extensions else ""
