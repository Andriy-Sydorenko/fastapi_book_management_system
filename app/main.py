from fastapi import Depends, FastAPI, HTTPException

from app.core.config import settings
from app.crud import books as crud_books
from app.schemas.books import BookList, BookQueryParams

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/books/", response_model=list[BookList])
async def list_books(
    query: BookQueryParams = Depends(),
    # TODO: add after implementing authentication
    # current_user: dict = Depends(get_current_user)  # Only authenticated users can access
):
    """
    Retrieve a list of books with filtering, sorting, and pagination.
    The query parameters are validated and parsed using the BookQueryParams model.
    """
    try:
        books = await crud_books.get_books(
            title=query.title,
            author=query.author,
            genre=query.genre,
            year_from=query.year_from,
            year_to=query.year_to,
            sort_by=query.sort_by,
            sort_order=query.sort_order,
            limit=query.limit,
            offset=query.offset,
        )
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving books: {e}")
