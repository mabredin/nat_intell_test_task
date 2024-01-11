from pydantic import BaseModel


class ProposalBase(BaseModel):
    title: str
    description: str
