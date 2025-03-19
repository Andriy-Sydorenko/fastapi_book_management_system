from fastapi import APIRouter, Depends, HTTPException, status

from app.crud.user import create_user_crud, get_current_user, verify_user_and_create_jwt
from app.schemas.user import UserCreate, UserDetail, UserLogin

router = APIRouter()


@router.post("/register/", response_model=UserDetail)
async def register(user: UserCreate):
    return await create_user_crud(user)


@router.post("/login/")
async def login(login_data: UserLogin):
    user = get_current_user()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token = await verify_user_and_create_jwt(login_data)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=UserDetail)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
