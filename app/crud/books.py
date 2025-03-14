from typing import Any, Optional

from fastapi import HTTPException

from app.schemas.books import BookCreate
from app.utils import get_connection


async def get_books(
    book_id: Optional[int] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    limit: int = 10,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """
    Retrieve books using the stored procedure 'get_books' with support for filtering,
    sorting, and pagination.

    Parameters:
        book_id (int, optional): Retrieve a single book by its ID.
        title (str, optional): Filter books by title (case-insensitive partial match).
        author (str, optional): Filter books by author name (case-insensitive partial match).
        genre (str, optional): Filter books by genre (exact match).
        year_from (int, optional): Filter books published from this year onwards.
        year_to (int, optional): Filter books published up to this year.
        sort_by (str): Column name to sort by. Allowed values: 'title', 'published_year', 'genre', 'isbn'.
        sort_order (str): Sort order: 'asc' or 'desc'.
        limit (int): Maximum number of records to return.
        offset (int): Number of records to skip (for pagination).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a book record.
    """
    conn = await get_connection()
    try:
        query = "SELECT * FROM get_books_procedure($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)"
        result = await conn.fetch(
            query,
            book_id,
            title,
            author,
            genre,
            year_from,
            year_to,
            sort_by,
            sort_order,
            limit,
            offset,
        )
        # Convert each asyncpg Record to a dictionary.
        return [dict(record) for record in result]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving books: {e}")
    finally:
        await conn.close()


async def create_book(book: BookCreate) -> [dict[str, Any]]:
    """
    Create a book using the stored procedure 'create_book_procedure'.
    Expects that the provided author already exists; otherwise, an exception is raised.
    """
    conn = await get_connection()
    try:
        query = "SELECT * FROM create_book_procedure($1, $2, $3, $4, $5)"
        result = await conn.fetch(
            query,
            book.title,
            book.isbn,
            book.published_year,
            book.genre,
            book.author_name,
        )
        if result:
            return dict(result[0])
        else:
            raise HTTPException(status_code=404, detail="Book creation failed: no record returned.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating book: {e}")
    finally:
        await conn.close()
