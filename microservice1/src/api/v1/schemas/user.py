from pydantic import BaseModel


class GetFullUser(BaseModel):
    id: int
    email: str | None = None
    username: str
    wallet_address: str
    block_number: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class CreateUser(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    wallet_address: str
    block_number: int
    is_superuser: bool = False


class GetUser(BaseModel):
    username: str
    email: str | None = None
    wallet_address: str
    block_number: int
    is_superuser: bool = False
    is_active: bool = True
