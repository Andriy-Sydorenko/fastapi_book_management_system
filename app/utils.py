import asyncpg

from app.core.config import settings


async def get_connection():
    """Helper function to establish a connection to the PostgreSQL database."""
    return await asyncpg.connect(settings.db_url)
