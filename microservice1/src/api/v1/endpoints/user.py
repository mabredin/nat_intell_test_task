from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.base import get_session
from db.models import User
from services.user import create_user, get_current_active_user, get_users

from ..schemas import user

user_router = APIRouter(tags=["user"])


@user_router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(session: AsyncSession = Depends(get_session)):
    return await get_users(session)


@user_router.get(
    "/users/me", status_code=status.HTTP_200_OK, response_model=user.GetFullUser
)
async def get_user(
    user: Annotated[User, Depends(get_current_active_user)],
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, dateil="Authentication failed"
        )
    return user


@user_router.post(
    "/auth/register", status_code=status.HTTP_201_CREATED, response_model=user.GetUser
)
async def create_new_user(
    new_user: user.CreateUser, session: AsyncSession = Depends(get_session)
) -> user.GetUser:
    return await create_user(new_user, session)
