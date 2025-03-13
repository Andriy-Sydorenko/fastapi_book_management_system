from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BookList(BaseModel):
    id: UUID
    title: str
    isbn: str
    published_year: int
    genre: str
    author_id: UUID
    author_name: Optional[str]

    class Config:
        from_attributes = True


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
