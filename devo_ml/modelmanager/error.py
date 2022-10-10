from __future__ import annotations

from pathlib import Path


class ModelManagerError(Exception):
    def __init__(self, code: int = None, msg: str = None):
        super().__init__(msg)
        self.code = code or 0
        self.msg = msg or ""

    @classmethod
    def from_code(cls, code: int, msg: str = None):
        if code == 5:
            return TokenError()
        return cls(code=code, msg=msg)

    def __str__(self):
        if self.code:
            return f"{self.code}: {self.msg}"
        return self.msg


class TokenError(ModelManagerError):
    def __init__(self):
        super().__init__(code=5, msg="Token invalid or expired")


class ModelNotFound(ModelManagerError):
    def __init__(self, model: str):
        super().__init__(msg=f"'{model}'")


class ModelAlreadyExists(ModelManagerError):
    def __init__(self, model: str):
        super().__init__(msg=f"'{model}'")


class ProfileError(ModelManagerError):
    def __init__(self, msg: str):
        super().__init__(msg=msg)


class ProfileValueRequired(ModelManagerError):
    def __init__(self, option: str):
        super().__init__(msg=f"'{option}'")
