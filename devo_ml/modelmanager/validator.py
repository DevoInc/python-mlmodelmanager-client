"""A set of convenient validators."""

import validators


def is_valid_url(url: str) -> bool:
    """Checks whether a URL is valid.

    :param url: URL to check
    :return: True if url is valid, False otherwise
    """
    return validators.url(url)
