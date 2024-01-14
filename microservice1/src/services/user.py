from typing import Annotated, Sequence

import httpx
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas import user as UserSchema
from config import second_service, token_settings
from db.base import get_session
from db.models import User


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


async def get_users(session: AsyncSession) -> Sequence[User]:
    query = select(User).order_by("id")
    result = await session.execute(query)
    return result.scalars().all()


async def get_current_user(
    token: Annotated[str, Depends(token_settings.oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            token_settings.SECRET_KEY_TOKEN,
            algorithms=[token_settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise credentials_exception
        return await get_user_by_id(user_id, session)
    except JWTError:
        raise credentials_exception


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def create_user(
    new_user: UserSchema.CreateUser, session: AsyncSession = Depends(get_session)
) -> UserSchema.GetUser:
    wallet = await is_exist_wallet(new_user, session)
    if wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким адресом кошелька существует",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_verified = second_service.verify_address(new_user.wallet_address)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Введеный адрес кошелька не существует",
            headers={"WWW-Authenticate": "Bearer"},
        )
    block_number = second_service.get_latest_block()
    user = User(
        username=new_user.username,
        hashed_password=token_settings.bcrypt_context.hash(new_user.hashed_password),
        email=new_user.email,
        wallet_address=new_user.wallet_address,
        block_number=block_number,
        is_superuser=new_user.is_superuser,
    )

    try:
        session.add(user)
        await session.commit()
        return UserSchema.GetUser(
            username=new_user.username,
            email=new_user.email,
            wallet_address=new_user.wallet_address,
            block_number=block_number,
            is_superuser=new_user.is_superuser,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо заполнить все поля",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def is_exist_wallet(
    new_user: UserSchema.CreateUser, session: AsyncSession = Depends(get_session)
) -> bool:
    query = select(User).where(User.wallet_address == new_user.wallet_address)
    result = await session.execute(query)
    user = result.scalars().first()
    if user:
        return True
    return False
