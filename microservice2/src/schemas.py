from pydantic import BaseModel
from web3.types import Wei


class GetBalance(BaseModel):
    balance: Wei


class GetInfoByBlock(BaseModel):
    number: int
    count_transactions: int
    difficulty: int
    time: str


class GetVerify(BaseModel):
    is_verified: bool
