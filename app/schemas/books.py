import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.crud.authors import get_authors


class BookDetail(BaseModel):
    id: int
    title: str
    isbn: str
    published_year: int
    genre: str
    author_id: int
    author_name: str

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    isbn: str
    published_year: int
    genre: str
    author_name: str

    @field_validator("author", check_fields=False)
    async def validate_author(cls, value):
        try:
            result = await get_authors(author_name=value)
        except Exception as e:
            raise ValueError(f"Error checking author: {str(e)}")
        if not result:
            raise ValueError(f"Author '{value}' does not exist.")
        return value

    @field_validator("title", check_fields=False)
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title can't be empty.")
        return value

    @field_validator("isbn", check_fields=False)
    def validate_isbn(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ISBN can't be empty.")
        if len(value) != 13:
            raise ValueError("ISBN must be 13 characters long.")
        return value

    @field_validator("genre", check_fields=False)
    def validate_genre(cls, value: str) -> str:
        if value not in ["Fiction", "Non-Fiction", "Science", "History"]:
            raise ValueError("Genre must be one of: Fiction, Non-Fiction, Science, History.")
        return value

    @field_validator("author", check_fields=False)
    def validate_author(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Author can't be empty.")
        # Optionally, you could add further validation here (e.g., checking against allowed names)
        return value

    @field_validator("published_year", check_fields=False)
    def validate_published_year(cls, value: int) -> int:
        current_year = datetime.datetime.now().year
        if value < 1800 or value > current_year:
            raise ValueError(f"Published year must be between 1800 and {current_year}.")
        return value


class BookQueryParams(BaseModel):
    title: Optional[str] = Field(None, description="Filter books by title (partial match)")
    author: Optional[str] = Field(None, description="Filter books by author name (partial match)")
    genre: Optional[str] = Field(None, description="Filter books by genre (exact match)")
    year_from: Optional[int] = Field(None, description="Filter books published from this year onward")
    year_to: Optional[int] = Field(None, description="Filter books published up to this year")
    sort_by: str = Field("created_at", description="Column to sort by (e.g., title, published_year, genre, isbn)")
    sort_order: str = Field("desc", description="Sort order: 'asc' or 'desc'")
    limit: int = Field(20, description="Maximum number of records to return")
    offset: int = Field(0, description="Offset for pagination")
