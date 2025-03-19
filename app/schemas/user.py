from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.validators import validate_email, validate_password


class UserBase(BaseModel):
    email: EmailStr = Field(..., min_length=1, max_length=255, description="Email address of the user")

    _validate_email = field_validator("email")(validate_email)


class UserDetail(UserBase):
    id: int
    full_name: str
    created_at: datetime


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=255, description="Password of the user")

    _validate_password = field_validator("password")(validate_password)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255, description="Password of the user")
    full_name: Optional[str] = Field("", min_length=1, max_length=255, description="Full name of the user")

    _validate_password = field_validator("password")(validate_password)
