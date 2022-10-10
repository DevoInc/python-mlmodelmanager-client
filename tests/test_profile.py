import pytest

from devo_ml.modelmanager.auth import STANDALONE, BEARER
from devo_ml.modelmanager.error import ProfileValueRequired, ProfileError
from devo_ml.modelmanager.profile import read_profile_from_file


@pytest.fixture
def profiles_file(abs_path):
    return abs_path("./profiles/profiles.ini")


def test_read_missing_profile(profiles_file):
    with pytest.raises(ProfileError):
        read_profile_from_file("missing_profile", profiles_file)


def test_read_profile_from_no_existing_file(abs_path):
    file = abs_path("profiles/no_existing_file.ini")
    with pytest.raises(ProfileError):
        read_profile_from_file("profile", file)


def test_read_profile_from_file(profiles_file):
    profile = read_profile_from_file("foo_profile", profiles_file)
    assert profile == {
        "url": "https://localhost",
        "token": "foo_profile_token",
        "auth_type": STANDALONE,
        "download_path": "/home/user/models",
    }
    profile = read_profile_from_file("bar_profile", profiles_file)
    assert profile == {
        "url": "https://localhost",
        "token": "bar_profile_token",
        "auth_type": BEARER,
        "download_path": None,
    }


def test_read_profile_from_file_with_no_auth_type(profiles_file):
    profile = read_profile_from_file("no_auth_type_profile", profiles_file)
    assert profile == {
        "url": "https://localhost",
        "token": "no_auth_type_profile_token",
        "auth_type": STANDALONE,
        "download_path": None,
    }


def test_read_profile_from_file_with_no_url(profiles_file):
    with pytest.raises(ProfileValueRequired):
        read_profile_from_file("no_url_profile", profiles_file)


def test_read_profile_from_file_with_no_token(profiles_file):
    with pytest.raises(ProfileValueRequired):
        read_profile_from_file("no_token_profile", profiles_file)


def test_read_profile_from_file_with_invalid_url(profiles_file):
    with pytest.raises(ProfileError):
        read_profile_from_file("invalid_url_profile", profiles_file)


def test_read_profile_from_file_with_invalid_auth_type(profiles_file):
    with pytest.raises(ProfileError):
        read_profile_from_file("invalid_auth_type_profile", profiles_file)


@pytest.mark.parametrize("f", [
    "./profiles/duplicate_profiles.ini",
    "./profiles/duplicate_profile_options.ini"
])
def test_read_profile_from_invalid_file(f, abs_path):
    file = abs_path(f)
    with pytest.raises(ProfileError):
        read_profile_from_file("invalid_auth_type_profile", file)
