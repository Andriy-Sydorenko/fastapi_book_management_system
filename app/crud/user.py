from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status

from app.crud.auth import create_jwt_token, decrypt_jwt, oauth2_scheme
from app.schemas.user import UserCreate, UserLogin
from app.utils import get_connection

ph = PasswordHasher()


async def get_user_by_email_crud(email: str) -> dict:
    conn = await get_connection()
    try:
        query = "SELECT * FROM get_user_by_email_function($1)"
        result = await conn.fetch(
            query,
            email,
        )
        return dict(result[0]) if result else {}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving user: {e}")
    finally:
        await conn.close()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    email = decrypt_jwt(token)
    user = await get_user_by_email_crud(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def create_user_crud(user_data: UserCreate) -> dict:
    user = await get_user_by_email_crud(user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = ph.hash(user_data.password)
    conn = await get_connection()
    try:
        query = "SELECT * FROM create_user_function($1, $2, $3)"
        result = await conn.fetch(
            query,
            user_data.email,
            hashed_password,
            user_data.full_name,
        )
        return dict(result[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")
    finally:
        await conn.close()


async def verify_user_and_create_jwt(user_data: UserLogin) -> str:
    try:
        user = await get_user_by_email_crud(user_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User with these credentials not found."
            )
        ph.verify(user["hashed_password"], user_data.password)

        token = create_jwt_token(user["email"])

    except VerifyMismatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user credentials!")

    return token
