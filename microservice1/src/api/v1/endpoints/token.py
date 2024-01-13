from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas.token import Token
from config import token_settings
from db.base import get_session
from services.token import authenticate_user, create_access_token

token_router = APIRouter(tags=["token"])


@token_router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Неправильный логин или пароль",
        )
    token = create_access_token(
        user.username,
        user.id,
        timedelta(minutes=token_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=token, token_type="bearer")
