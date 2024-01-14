from decimal import Decimal
from typing import Any

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas import vote
from config import second_service
from db.models import User, Vote


async def create_vote(
    proposal_id: int, user: User, data: vote.VoteCreate, session: AsyncSession
) -> vote.VoteGet:
    await check_if_user_votes(user, proposal_id, session)

    user_balance = await check_and_return_balance(user.wallet_address)
    block_number = second_service.get_latest_block()

    await create(user.id, proposal_id, user_balance, block_number, data, session)

    return vote.VoteGet(
        proposal_id=proposal_id,
        user_id=user.id,
        is_like=data.is_like,
        user_balance=user_balance,
        block_number=block_number,
    )


async def check_if_user_votes(
    user: User, proposal_id: int, session: AsyncSession
) -> None:
    result = await get_vote_by_proposal_and_user(user.id, proposal_id, session)
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже голосовали",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_vote_by_proposal_and_user(
    user_id: int, proposal_id: int, session: AsyncSession
) -> (Vote | None):
    query = select(Vote).filter_by(proposal_id=proposal_id, user_id=user_id)
    result = await session.execute(query)
    return result.scalars().one_or_none()


async def create(
    user_id: int,
    proposal_id: int,
    user_balance: Decimal,
    block_number: int,
    data: vote.VoteCreate,
    session: AsyncSession,
) -> None:
    stmt = Vote(
        proposal_id=proposal_id,
        user_id=user_id,
        is_like=data.is_like,
        user_balance=user_balance,
        block_number=block_number,
    )
    try:
        session.add(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def check_and_return_balance(address: str) -> Decimal:
    balance = second_service.get_balance(address)
    balance = Decimal(balance)
    if not balance > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Для голосования ваш баланс должен быть больше 0",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return balance
