from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ENCRYPTION_ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def create_jwt_token(user_email: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_data = {"sub": user_email, "exp": expire}
    return jwt.encode(user_data, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)


def decrypt_jwt(token: str = Depends(oauth2_scheme)) -> str:
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ENCRYPTION_ALGORITHM])
        return decoded_data["sub"]
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
