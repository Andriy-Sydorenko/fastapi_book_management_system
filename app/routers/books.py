from fastapi import APIRouter, Depends, HTTPException

from app.crud.books import (
    create_book_crud,
    delete_book_crud,
    get_books_crud,
    update_book_crud,
)
from app.schemas.books import BookCreate, BookDetail, BookQueryParams, BookUpdate

router = APIRouter(prefix="/books")


@router.get("/", response_model=list[BookDetail])
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
        books = await get_books_crud(
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
        raise HTTPException(status_code=400, detail=f"Error retrieving books: {e}")


@router.get("/{book_id}/", response_model=BookDetail)
async def get_book(book_id: int):
    try:
        book = await get_books_crud(book_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving book: {e}")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book[0]


@router.post("/", response_model=BookDetail)
async def create_book(book: BookCreate):
    try:
        new_book = await create_book_crud(book)
        return new_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating book: {e}")


@router.put("/{book_id}/", response_model=BookDetail)
async def update_book(book_id: int, book: BookUpdate):
    try:
        updated_book = await update_book_crud(book_id, book)
        return updated_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating book: {e}")


@router.delete("/{book_id}/", response_model=dict[str, str])
async def delete_book(book_id: int):
    try:
        await delete_book_crud(book_id)
        return {"message": "Book deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting book: {e}")
