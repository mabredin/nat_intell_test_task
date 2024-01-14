from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.schemas import vote
from db.base import get_session
from db.models import User
from services import vote as VotelService
from services.user import get_current_active_user

vote_router = APIRouter(tags=["vote"])


@vote_router.post(
    "/votes/{proposal_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=vote.VoteGet,
)
async def create_vote(
    proposal_id: int,
    user: Annotated[User, Depends(get_current_active_user)],
    data: vote.VoteCreate = None,
    session: AsyncSession = Depends(get_session),
):
    return await VotelService.create_vote(proposal_id, user, data, session)
