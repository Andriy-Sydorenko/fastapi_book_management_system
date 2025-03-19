from fastapi import FastAPI

from app.core.config import settings
from app.routers import author, book, user

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.include_router(book.router, prefix="/api")
app.include_router(author.router, prefix="/api")
app.include_router(user.router, prefix="/api")
