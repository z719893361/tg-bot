from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from admin.auth.oauth2 import create_access_token
from db import crud, get_db
from models.form.login import LoginForm
from models.response import Result


router = APIRouter(tags=['登录接口'])


@router.post("/login", name='登录接口')
async def login_for_access_token(form_data: LoginForm, db: AsyncSession = Depends(get_db)):
    user = await crud.user.get_user_login(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"username": user.username}
    )
    return Result.ok("登录成功", data={"access_token": access_token})


