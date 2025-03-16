from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.core.validators import validate_author, validate_genre, validate_published_year


class BookBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Title of the book")
    isbn: Optional[str] = Field(None, min_length=13, max_length=13, description="ISBN of the book")
    published_year: Optional[int] = Field(None, description="Year the book was published")
    genre: Optional[str] = Field(None, min_length=1, max_length=50, description="Genre of the book")
    author_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Name of the author")

    _validate_published_year = field_validator("published_year")(validate_published_year)
    _validate_genre = field_validator("genre")(validate_genre)
    _validate_author = field_validator("author_name")(validate_author)

    class Config:
        validate_assignment = True


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


class BookCreate(BookBase):
    title: str
    isbn: str
    published_year: int
    genre: str
    author_name: str


class BookUpdate(BookBase):
    pass


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
