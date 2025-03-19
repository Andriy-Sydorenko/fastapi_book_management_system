from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.crud.author import (
    create_author_crud,
    delete_author_crud,
    get_authors_crud,
    update_author_crud,
)
from app.crud.user import get_current_user
from app.schemas.author import AuthorCreate, AuthorDetail

router = APIRouter(prefix="/authors")


@router.get("/", response_model=list[AuthorDetail])
async def list_authors():
    try:
        authors = await get_authors_crud()
        return authors
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving authors: {e}")


@router.get("/{author_id}/", response_model=AuthorDetail)
async def get_author(author_id: int):
    try:
        author = await get_authors_crud(author_id=author_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving author: {e}")
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    return author[0]


@router.post("/", status_code=201, response_model=AuthorDetail)
async def create_author(author: AuthorCreate, current_user: dict = Depends(get_current_user)):
    try:
        existing_authors = await get_authors_crud(author_name=author.name)
        if existing_authors:
            raise HTTPException(status_code=400, detail="Author name must be unique. Provided name already exists.")
        new_author = await create_author_crud(author)
        return new_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error checking for unique author: {e}")


@router.put("/{author_id}/", response_model=AuthorDetail)
async def update_author(author_id: int, author: AuthorCreate, current_user: dict = Depends(get_current_user)):
    try:
        existing_authors = await get_authors_crud(author_id=author_id)
        if not existing_authors:
            raise HTTPException(status_code=404, detail="Author not found.")
        updated_author = await update_author_crud(author_id, author)
        return updated_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating author: {e}")


@router.delete(
    "/{author_id}/",
    responses={
        200: {
            "description": "Author deleted successfully.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"message": {"type": "string", "example": "Author deleted successfully"}},
                    }
                }
            },
        },
    },
)
async def delete_author(author_id: int, current_user: dict = Depends(get_current_user)):
    try:
        await delete_author_crud(author_id)
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting author: {e}")
