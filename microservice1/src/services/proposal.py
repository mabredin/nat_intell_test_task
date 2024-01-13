from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.proposal import ProposalBase as ProposalSchema
from db.models import Proposal


async def get_proposals(session: AsyncSession):
    query = select(Proposal).order_by("id")
    result = await session.execute(query)
    return result.scalars().all()


async def create_proposal(
    data: ProposalSchema, session: AsyncSession
) -> dict[str, str]:
    # Нужна проверка на суперадмина

    proposal = Proposal(title=data.title, description=data.description)
    try:
        session.add(proposal)
        await session.commit()
    except Exception as e:
        print(e)

    return {"status": "success"}
