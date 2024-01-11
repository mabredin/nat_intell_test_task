from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.models import Proposal as ProposalModel
from sqlalchemy.orm import Session

from api.v1.schemas.proposal import ProposalBase as ProposalSchema


def create_proposal(data: ProposalSchema, db: Session):
    proposal = ProposalModel(
        title = data.title,
        description = data.description
    )
    try:
        db.add(proposal)
        db.commit()
        db.refresh(proposal)
    except Exception as e:
        print(e)
    
    return proposal

async def get_proposals(db: AsyncSession):
    result = await db.execute(select(ProposalModel))
    return result.scalars().all()


async def create_proposal(data: ProposalSchema, db: AsyncSession):
    proposal = ProposalModel(
        title = data.title,
        description = data.description
    )
    try:
        db.add(proposal)
        await db.commit()
    except Exception as e:
        print(e)
    
    return proposal
