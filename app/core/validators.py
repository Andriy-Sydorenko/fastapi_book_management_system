import datetime


def validate_genre(cls, value: str) -> str:
    if value not in ["Fiction", "Non-Fiction", "Science", "History"]:
        raise ValueError("Genre must be one of: Fiction, Non-Fiction, Science, History.")
    return value


def validate_published_year(value: int) -> int:
    current_year = datetime.datetime.now().year
    if value < 1800 or value > current_year:
        raise ValueError(f"Published year must be between 1800 and {current_year}.")
    return value


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters.")
    return value


def validate_email(value: str) -> str:
    if not value.strip():
        raise ValueError("Email address can't be empty.")
    if "@" not in value:
        raise ValueError("Invalid email address.")
    return value
