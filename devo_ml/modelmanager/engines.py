from typing import Sequence


H2O = "H2O"
BIGML = "BIGML"
DL4J = "DL4J"
CATBOOST = "CATBOOST"
DEEPLOGCORE = "DEEPLOGCORE"
DEEPLOGAPP = "DEEPLOGAPP"
DT = "DT"
IDA = "IDA"
MLSTATS = "MLSTATS"
MUA = "MUA"
ONNX = "ONNX"
UNICODE = "UNICODE"
WORKFLOWS = "WORKFLOWS"


_aware_engines = {
    H2O: {
        "code": H2O,
        "extensions": [".zip"],
    },
    BIGML: {
        "code": BIGML,
        "extensions": [".json"],
    },
    DL4J: {
        "code": DL4J,
        "extensions": [".h5"],
    },
    CATBOOST: {
        "code": CATBOOST,
        "extensions": [".cbm"],
    },
    DEEPLOGCORE: {
        "code": DEEPLOGCORE,
        "extensions": [".zip"],
    },
    DEEPLOGAPP: {
        "code": DEEPLOGAPP,
        "extensions": [".zip"],
    },
    DT: {
        "code": DT,
        "extensions": [".json"],
    },
    IDA: {
        "code": IDA,
        "extensions": [".json"],
    },
    MLSTATS: {
        "code": MLSTATS,
        "extensions": [],
    },
    MUA: {
        "code": MUA,
        "extensions": [".zip"],
    },
    ONNX: {
        "code": ONNX,
        "extensions": [".onnx"],
    },
    UNICODE: {
        "code": UNICODE,
        "extensions": [".zip"],
    },
    WORKFLOWS: {
        "code": WORKFLOWS,
        "extensions": [".json"],
    },
}


def get_engine_extensions(engine_code: str) -> Sequence[str]:
    engine = _aware_engines.get(engine_code.upper())
    return engine.get("extensions", []) if engine else []


def get_default_engine_extension(engine_code: str) -> str:
    extensions = get_engine_extensions(engine_code)
    return extensions[0] if extensions else ""
