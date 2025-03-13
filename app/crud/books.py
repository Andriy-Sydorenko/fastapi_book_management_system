from typing import Any, Optional

from app.utils import get_connection


async def get_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    sort_by: str = "title",
    sort_order: str = "asc",
    limit: int = 10,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """
    Retrieve books using the stored procedure 'get_books' with support for filtering,
    sorting, and pagination.

    Parameters:
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
        # Call the stored procedure using positional parameters.
        # The stored procedure 'get_books' is defined to accept 9 parameters.
        query = "SELECT * FROM get_books($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        result = await conn.fetch(
            query,
            title,  # p_title
            author,  # p_author
            genre,  # p_genre
            year_from,  # p_year_from
            year_to,  # p_year_to
            sort_by,  # p_sort_by
            sort_order,  # p_sort_order
            limit,  # p_limit
            offset,  # p_offset
        )
        # Convert each asyncpg Record to a dictionary.
        return [dict(record) for record in result]
    finally:
        await conn.close()
        return []
