from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import TextClause, delete, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette import status

from api.v1.schemas import proposal, vote
from db.models import Proposal, User, Vote


async def get_proposals(user: User, session: AsyncSession) -> Sequence[Proposal]:
    query = select(Proposal).order_by("id")
    result = await session.execute(query)
    return result.scalars().all()


async def create_proposal(
    user: User, data: proposal.ProposalCreateUpdate, session: AsyncSession
) -> proposal.ProposalCreateUpdate:
    await check_superuser(user)
    stmt = Proposal(title=data.title, description=data.description)
    try:
        session.add(stmt)
        await session.commit()
        return proposal.ProposalCreateUpdate(
            title=data.title, description=data.description
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def update_proposal(
    proposal_id: int,
    user: User,
    data: proposal.ProposalCreateUpdate,
    session: AsyncSession,
) -> proposal.ProposalCreateUpdate:
    await check_superuser_and_number_votes(proposal_id, user, session)
    stmt = (
        update(Proposal)
        .values(title=data.title, description=data.description)
        .filter_by(id=proposal_id)
    )
    try:
        await session.execute(stmt)
        await session.commit()
        return proposal.ProposalCreateUpdate(
            id=proposal_id, title=data.title, description=data.description
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def delete_proposal(proposal_id: int, user: User, session: AsyncSession) -> None:
    await check_superuser_and_number_votes(proposal_id, user, session)
    stmt = delete(Proposal).filter_by(id=proposal_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def check_superuser(user: User) -> (HTTPException | None):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            headers={"WWW-Authenticate": "Bearer"},
        )


async def check_superuser_and_number_votes(
    proposal_id: int, user: User, session: AsyncSession
) -> None:
    await check_superuser(user)

    query = select(count()).select_from(Vote).filter_by(proposal_id=proposal_id)
    try:
        result = await session.execute(query)
        result = result.scalars().one()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if result:
        times = "time" if result == 1 else "times"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This proposal has already been voted for {result} {times}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_voting_count_info(
    proposal_id: int, session: AsyncSession
) -> vote.VoteResult:
    query = text(
        """
        SELECT
            COALESCE(like_count, 0) AS true_count,
            COALESCE(dislike_count, 0) AS false_count
        FROM (
            SELECT
                COUNT(*) AS like_count
            FROM vote
            WHERE is_like = true
            AND proposal_id = :id
        ) AS like_subquery
        LEFT JOIN (
            SELECT 
                count(*) as dislike_count
            FROM vote
            WHERE is_like = false
            and proposal_id = :id
        ) AS dislike_subquery ON true
        WHERE exists (
            SELECT 
                null
            FROM proposal
            WHERE id = :id
        );
        """
    )
    return await get_voting_info(proposal_id, query, session)


async def get_voting_balance_info(
    proposal_id: int, session: AsyncSession
) -> vote.VoteResult:
    query = text(
        """
        SELECT
            COALESCE(like_balance, 0) AS true_count,
            COALESCE(dislike_balance, 0) AS false_count
        FROM (
            SELECT
                sum(user_balance) AS like_balance
            FROM vote
            WHERE is_like = true
            AND proposal_id = :id
        ) AS like_subquery
        LEFT JOIN (
            SELECT 
                sum(user_balance) as dislike_balance
            FROM vote
            WHERE is_like = false
            and proposal_id = :id
        ) AS dislike_subquery ON true
        WHERE exists (
            SELECT null
            FROM proposal
            WHERE id = :id
        );
        """
    )
    return await get_voting_info(proposal_id, query, session)


async def get_voting_info(
    proposal_id: int, query: TextClause, session: AsyncSession
) -> vote.VoteResult:
    try:
        query = query.bindparams(id=proposal_id)
        result = await session.execute(query)
        result = result.one_or_none()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при отправке запроса в БД",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанный id не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    likes_count, dislikes_count = result
    return vote.VoteResult(
        proposal_id=proposal_id, likes_count=likes_count, dislikes_count=dislikes_count
    )
