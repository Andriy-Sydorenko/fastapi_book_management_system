import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.utils import get_unique_email


@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        unique_email = get_unique_email()
        register_payload = {"email": unique_email, "password": "strongpassword", "full_name": "Test User"}
        response = await client.post("/api/register/", json=register_payload)
        assert response.status_code == status.HTTP_200_OK, response.text
        user_data = response.json()
        assert "id" in user_data
        assert user_data["email"] == unique_email

        login_payload = {"email": unique_email, "password": "strongpassword"}
        response = await client.post("/api/login/", json=login_payload)
        assert response.status_code == status.HTTP_200_OK, response.text
        token_data = response.json()
        assert "access_token" in token_data


@pytest.mark.asyncio
async def test_get_current_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        unique_email = get_unique_email()
        register_payload = {"email": unique_email, "password": "strongpassword", "full_name": "Me"}
        response = await client.post("/api/register/", json=register_payload)
        assert response.status_code == status.HTTP_200_OK, response.text

        login_payload = {"email": unique_email, "password": "strongpassword"}
        response = await client.post("/api/login/", json=login_payload)
        token_data = response.json()
        access_token = token_data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        response = await client.get("/api/me/", headers=headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        user_data = response.json()
        assert user_data["email"] == unique_email
