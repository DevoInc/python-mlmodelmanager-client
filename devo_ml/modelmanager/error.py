"""A set of exceptions raised by ML Model Manager."""

from __future__ import annotations


class ModelManagerError(Exception):
    """Any error of ML Model Manager."""

    def __init__(self, code: int = None, msg: str = None) -> None:
        """Creates a :class:`ModelManagerError`.

        :param code: The code of the error
        :param msg: Any message describing the error
        """
        super().__init__(msg)
        self.code = code or 0
        self.msg = msg or ""

    @classmethod
    def from_code(cls, code: int, msg: str = None) -> ModelManagerError:
        """Creates an error associates with a code.

        :param code: The code of the error
        :param msg: Any message describing the error
        :return: An exception associate with the code
        """
        if code == 5:
            return TokenError()
        return cls(code=code, msg=msg)

    def __str__(self) -> str:
        """String representation of the error.

        :return: The string representation of the error
        """
        if self.code:
            return f"{self.code}: {self.msg}"
        return self.msg


class TokenError(ModelManagerError):
    """Any error with an access token."""

    def __init__(self) -> None:
        """Creates a :class:`TokenError`."""
        super().__init__(code=5, msg="Token invalid or expired")


class ModelNotFound(ModelManagerError):
    """Indicates that a model does not exist in the system."""

    def __init__(self, model: str):
        """Creates a :class:`ModelNotFound`.

        :param model: The missing model name
        """
        super().__init__(msg=f"'{model}'")


class ModelAlreadyExists(ModelManagerError):
    """Indicates that a model already exists in the system."""

    def __init__(self, model: str):
        """Creates a :class:`ModelAlreadyExists`.

        :param model: The duplicate model name
        """
        super().__init__(msg=f"'{model}'")


class ProfileError(ModelManagerError):
    """Any profile error."""

    def __init__(self, msg: str):
        """Creates a :class:`ProfileError`.

        :param msg: Any message describing the error
        """
        super().__init__(msg=msg)


class ProfileValueRequired(ModelManagerError):
    """Indicates an error with a mandatory value of a profile"""

    def __init__(self, option: str):
        """Creates a :class:`ProfileValueRequired`.

        :param option: The option causing the error
        """
        super().__init__(msg=f"'{option}'")
