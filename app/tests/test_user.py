import datetime

import pytest

from app.crud.user import create_user_crud, get_user_by_email_crud
from app.schemas.user import UserCreate
from app.utils import get_unique_email


class FakeUserConnection:
    async def fetch(self, query, *args, **kwargs):
        if "get_user_by_email_function" in query:
            email = args[0]
            if email == "existing@example.com":
                return [
                    {
                        "id": 1,
                        "email": email,
                        "hashed_password": "hashedpassword",
                        "full_name": "Existing User",
                        "created_at": datetime.datetime.now(),
                    }
                ]
            return []  # Simulate no user found for new email
        elif "create_user_function" in query:
            # Return a dummy record for user creation
            return [
                {
                    "id": 2,
                    "email": args[0],
                    "hashed_password": args[1],
                    "full_name": args[2],
                    "created_at": datetime.datetime.now(),
                }
            ]
        return []

    async def close(self):
        pass


@pytest.fixture(autouse=True)
def fake_db_user(monkeypatch):
    async def fake_get_connection():
        return FakeUserConnection()

    import app.utils

    monkeypatch.setattr(app.utils, "get_connection", fake_get_connection)


@pytest.mark.asyncio
async def test_get_user_by_email_crud_not_found():
    user = await get_user_by_email_crud("nonexistent@example.com")
    assert user == {}


@pytest.mark.asyncio
async def test_create_user_crud_success():
    user_data = UserCreate(email=get_unique_email(), password="strongpassword", full_name="New User")
    created_user = await create_user_crud(user_data)
    assert created_user["email"] == user_data.email
    assert created_user["full_name"] == "New User"
