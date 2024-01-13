from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas import proposal, vote
from db.base import get_session
from db.models import User
from services import proposal as ProposalService
from services.user import get_current_active_user

proposal_router = APIRouter(tags=["proposal"])


@proposal_router.get("/proposals", status_code=status.HTTP_200_OK)
async def get_proposals(
    user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.get_proposals(user, session)


@proposal_router.post(
    "/proposals",
    status_code=status.HTTP_201_CREATED,
    response_model=proposal.ProposalCreateUpdate,
)
async def create_proposal(
    user: Annotated[User, Depends(get_current_active_user)],
    data: proposal.ProposalCreateUpdate = None,
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.create_proposal(user, data, session)


@proposal_router.put(
    "/proposals/{proposal_id}",
    status_code=status.HTTP_200_OK,
    response_model=proposal.ProposalCreateUpdate,
)
async def update_proposal(
    proposal_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    data: proposal.ProposalCreateUpdate = None,
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.update_proposal(proposal_id, user, data, session)


@proposal_router.delete(
    "/proposals/{proposal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_proposal(
    proposal_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.delete_proposal(proposal_id, user, session)


@proposal_router.get(
    "/proposals/{proposal_id}/votes/counts",
    status_code=status.HTTP_200_OK,
    response_model=vote.VoteResult,
)
async def get_voting_count_info(
    proposal_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.get_voting_count_info(proposal_id, session)


@proposal_router.get(
    "/proposals/{proposal_id}/votes/balances",
    status_code=status.HTTP_200_OK,
    response_model=vote.VoteResult,
)
async def get_voting_balance_info(
    proposal_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    return await ProposalService.get_voting_balance_info(proposal_id, session)
