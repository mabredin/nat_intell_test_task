import datetime
from decimal import Decimal

from pydantic import BaseModel


class VoteBase(BaseModel):
    proposal_id: int
    user_id: int
    is_like: bool = False
    created_at: datetime.datetime
    user_balance: Decimal
    block_number: int


class VoteGet(BaseModel):
    proposal_id: int
    user_id: int
    is_like: bool = False
    user_balance: Decimal
    block_number: int


class VoteCreate(BaseModel):
    proposal_id: int
    is_like: bool = False


class VoteResult(BaseModel):
    proposal_id: int | None
    likes_count: int = 0
    dislikes_count: int = 0
