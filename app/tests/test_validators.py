import datetime

import pytest

from app.core.validators import (
    validate_email,
    validate_genre,
    validate_password,
    validate_published_year,
)

# Synchronous validators


@pytest.mark.parametrize("email", ["user@example.com", "test@domain.com"])
def test_validate_email_success(email: str):
    assert validate_email(email) == email


@pytest.mark.parametrize("email", ["", "   ", "invalidemail.com"])
def test_validate_email_failure(email: str):
    with pytest.raises(ValueError):
        validate_email(email)


def test_validate_password_success():
    password = "strongpassword"
    assert validate_password(password) == password


def test_validate_password_failure():
    with pytest.raises(ValueError):
        validate_password("short")


def test_validate_genre_success():
    for genre in ["Fiction", "Non-Fiction", "Science", "History"]:
        assert validate_genre(None, genre) == genre


def test_validate_genre_failure():
    with pytest.raises(ValueError):
        validate_genre(None, "Drama")


def test_validate_published_year_success():
    current_year = datetime.datetime.now().year
    valid_year = current_year - 5
    assert validate_published_year(valid_year) == valid_year


@pytest.mark.parametrize("year", [1700, datetime.datetime.now().year + 1])
def test_validate_published_year_failure(year: int):
    with pytest.raises(ValueError):
        validate_published_year(year)
