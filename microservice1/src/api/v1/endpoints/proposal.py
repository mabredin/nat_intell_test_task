from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_session
from services import proposal as ProposalService
from api.v1.schemas import proposal

proposal_router = APIRouter(
    tags=["proposal"],
)


@proposal_router.get('/')
async def get_proposals(db: AsyncSession = Depends(get_session)):
    return await ProposalService.get_proposals(db)


@proposal_router.post('/')
async def create_proposal(data: proposal.ProposalBase = None, db: AsyncSession = Depends(get_session)):
    return await ProposalService.create_proposal(data, db)
