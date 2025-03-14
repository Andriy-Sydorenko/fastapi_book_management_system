from typing import Any

from fastapi import HTTPException

from app.schemas.authors import AuthorCreate
from app.utils import get_connection


async def get_authors(author_id: int = None, author_name: str = None) -> [dict[str, Any]]:
    conn = await get_connection()
    try:
        query = "SELECT * FROM get_authors_procedure($1, $2)"
        result = await conn.fetch(query, author_id, author_name)
        return [dict(record) for record in result]
    finally:
        await conn.close()


async def create_author_crud(author: AuthorCreate) -> dict[str, Any]:
    conn = await get_connection()
    try:
        query = "SELECT * FROM create_author_procedure($1)"
        result = await conn.fetch(query, author.name)
        if result:
            return dict(result[0])
        else:
            raise Exception("Author creation failed: no record returned.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating author: {e}")
    finally:
        await conn.close()
