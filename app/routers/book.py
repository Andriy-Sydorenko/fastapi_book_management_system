import csv
import io
import json
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from app.crud.author import get_authors_crud
from app.crud.book import (
    create_book_crud,
    delete_book_crud,
    get_books_crud,
    update_book_crud,
)
from app.crud.user import get_current_user
from app.schemas.book import BookCreate, BookDetail, BookQueryParams, BookUpdate

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


@router.post("/", response_model=BookDetail)
async def create_book(book: BookCreate, current_user: dict = Depends(get_current_user)):
    author = await get_authors_crud(author_name=book.author_name)
    if not author:
        raise HTTPException(status_code=400, detail="Author not found. Please create the author first.")
    new_book = await create_book_crud(book)
    return new_book


@router.post("/import/", response_model=list[BookDetail])
async def import_books(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """
    Import books from a JSON or CSV file.
    JSON file must contain a list of objects matching the BookCreate schema.
    CSV file must have a header with columns: title, isbn, published_year, genre, author_name.
    """
    imported_books = []

    content = await file.read()
    if file.filename.lower().endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8"))
            if not isinstance(data, list):
                raise HTTPException(status_code=400, detail="JSON file must contain a list of books.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing JSON file: {e}")
    elif file.filename.lower().endswith(".csv"):
        try:
            decoded = content.decode("utf-8").splitlines()
            reader = csv.DictReader(decoded)
            data = list(reader)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {e}")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only JSON and CSV are accepted.")

    for record in data:
        try:
            book_data = BookCreate(**record)
            book_record = await create_book_crud(book_data)
            imported_books.append(book_record)
        except Exception as e:
            print(f"Failed to import record: {record} \nError: {e}")
            continue

    return JSONResponse(status_code=200, content=imported_books)


@router.get(
    "/export/",
    responses={
        200: {
            "description": "Successful file export. Returns a CSV or JSON file.",
            "content": {"text/csv": {}, "application/json": {}},
        },
        400: {"description": "Invalid file extension. Use 'json' or 'csv'."},
    },
)
async def export_books(
    export_file_ext: Optional[str] = Query("json", pattern="^(json|csv)$"),
):
    """
    Export books in JSON or CSV format.
    """
    books = await get_books_crud()

    if export_file_ext == "csv":
        output = io.StringIO()
        fieldnames = ["id", "title", "isbn", "published_year", "genre", "author_id", "author_name"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            writer.writerow(book)
        output.seek(0)
        headers = {"Content-Disposition": "attachment; filename=books.csv"}
        return StreamingResponse(output, media_type="text/csv", headers=headers)
    elif export_file_ext == "json":
        output = io.StringIO()
        json.dump(books, output)
        output.seek(0)
        headers = {"Content-Disposition": "attachment; filename=books.json"}
        return StreamingResponse(output, media_type="application/json", headers=headers)

    return JSONResponse(status_code=400, content={"message": "Invalid file extension. Use 'json' or 'csv'."})


@router.put("/{book_id}/", response_model=BookDetail)
async def update_book(book_id: int, book: BookUpdate, current_user: dict = Depends(get_current_user)):
    updated_book = await update_book_crud(book_id, book)
    return updated_book


@router.delete(
    "/{book_id}/",
    responses={
        200: {
            "description": "Book deleted successfully.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"message": {"type": "string", "example": "Book deleted successfully"}},
                    }
                }
            },
        },
    },
)
async def delete_book(book_id: int, current_user: dict = Depends(get_current_user)):
    await delete_book_crud(book_id)
    return JSONResponse(status_code=200, content={"message": "Book deleted successfully"})


@router.get("/{book_id}/", response_model=BookDetail)
async def get_book(book_id: int):
    try:
        book = await get_books_crud(book_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving book: {e}")
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book[0]
