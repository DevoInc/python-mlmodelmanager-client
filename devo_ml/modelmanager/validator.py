import validators


def is_valid_url(url: str) -> bool:
    """Checks whether a URL is valid.

    :param url: URL to check
    :type url: str
    :return: True if url is valid, False otherwise
    :rtype: bool
    """
    return validators.url(url)
