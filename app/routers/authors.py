from fastapi import APIRouter, HTTPException

from app.crud.authors import create_author_crud, get_authors
from app.schemas.authors import AuthorCreate, AuthorDetail

router = APIRouter(prefix="/authors")


@router.get("/", response_model=list[AuthorDetail])
async def list_authors():
    try:
        authors = await get_authors()
        return authors
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving authors: {e}")


@router.get("/{author_id}/", response_model=AuthorDetail)
async def get_author(author_id: int):
    try:
        author = await get_authors(author_id=author_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving author: {e}")
    if not author:
        raise HTTPException(status_code=404, detail="Author not found.")
    return author[0]


@router.post("/", status_code=201, response_model=AuthorDetail)
async def create_author(author: AuthorCreate):
    try:
        existing_authors = await get_authors(author_name=author.name)
        if existing_authors:
            raise HTTPException(status_code=400, detail="Author name must be unique. Provided name already exists.")
        new_author = await create_author_crud(author)
        return new_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error checking for unique author: {e}")
