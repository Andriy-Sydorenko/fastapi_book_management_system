import datetime

from app.crud.authors import get_authors_crud


async def validate_author(value):
    try:
        result = await get_authors_crud(author_name=value)
    except Exception as e:
        raise ValueError(f"Error checking author: {str(e)}")
    if not result:
        raise ValueError(f"Author '{value}' does not exist.")
    return value


def validate_genre(cls, value: str) -> str:
    if value not in ["Fiction", "Non-Fiction", "Science", "History"]:
        raise ValueError("Genre must be one of: Fiction, Non-Fiction, Science, History.")
    return value


def validate_published_year(value: int) -> int:
    current_year = datetime.datetime.now().year
    if value < 1800 or value > current_year:
        raise ValueError(f"Published year must be between 1800 and {current_year}.")
    return value
