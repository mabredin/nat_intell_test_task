from decimal import Decimal

from pydantic import BaseModel


class GetBalance(BaseModel):
    balance: int | Decimal


class GetInfoByBlock(BaseModel):
    number: int
    count_transactions: int
    difficulty: int
    time: str


class GetVerify(BaseModel):
    is_verified: bool
