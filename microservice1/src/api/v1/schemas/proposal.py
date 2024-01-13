from pydantic import BaseModel


class ProposalCreateUpdate(BaseModel):
    title: str
    description: str


class ProposalDelete(BaseModel):
    id: int
