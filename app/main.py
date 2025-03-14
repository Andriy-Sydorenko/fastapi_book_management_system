from fastapi import FastAPI

from app.core.config import settings
from app.routers import authors, books

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(books.router, prefix="/api")
app.include_router(authors.router, prefix="/api")
