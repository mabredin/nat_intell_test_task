from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.base import get_session
from db.models import User
from services.user import create_user, get_current_active_user, get_users

from ..schemas.user import CreateUserRequest

user_router = APIRouter(tags=["user"])


@user_router.get("/users")
async def get_all_users(session: AsyncSession = Depends(get_session)):
    return await get_users(session)


@user_router.get("/users/me", status_code=status.HTTP_200_OK)
async def get_user(
    user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, dateil="Authentication failed"
        )
    return user


@user_router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def create_new_user(
    new_user: CreateUserRequest, session: AsyncSession = Depends(get_session)
):
    return await create_user(new_user, session)
