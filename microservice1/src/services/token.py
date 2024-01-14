from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy import select

from config import token_settings
from db.models import User


async def authenticate_user(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], session
):
    query = select(User).where(User.username == data.username)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        return False
    if not token_settings.bcrypt_context.verify(data.password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expires_delta: timedelta | None = None
) -> str:
    payload = {"sub": username, "id": user_id}
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expires})
    return jwt.encode(
        payload, token_settings.SECRET_KEY_TOKEN, algorithm=token_settings.ALGORITHM
    )
