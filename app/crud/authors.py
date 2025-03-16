from typing import Any

from fastapi import HTTPException

from app.schemas.authors import AuthorCreate
from app.utils import get_connection


async def get_authors_crud(author_id: int = None, author_name: str = None) -> [dict[str, Any]]:
    conn = await get_connection()
    try:
        query = "SELECT * FROM get_authors_function($1, $2)"
        result = await conn.fetch(query, author_id, author_name)
        return [dict(record) for record in result]
    finally:
        await conn.close()


async def create_author_crud(author: AuthorCreate) -> dict[str, Any]:
    conn = await get_connection()
    try:
        query = "SELECT * FROM create_author_function($1)"
        result = await conn.fetch(query, author.name)
        if result:
            return dict(result[0])
        else:
            raise Exception("Author creation failed: no record returned.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating author: {e}")
    finally:
        await conn.close()


async def update_author_crud(author_id: int, author: AuthorCreate) -> dict[str, Any]:
    conn = await get_connection()
    try:
        query = "SELECT * FROM update_author_function($1, $2)"
        result = await conn.fetch(query, author_id, author.name)
        if result:
            return dict(result[0])
        else:
            raise Exception("Author update failed: no record returned.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating author: {e}")
    finally:
        await conn.close()


async def delete_author_crud(author_id: int) -> None:
    conn = await get_connection()
    try:
        query = "SELECT * FROM delete_author_function($1)"
        await conn.fetch(query, author_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting author: {e}")
    finally:
        await conn.close()
