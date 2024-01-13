from pydantic import BaseModel


class GetUserRequest(BaseModel):
    id: int
    email: str | None = None
    username: str
    wallet_address: str
    block_number: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class CreateUserRequest(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    wallet_address: str
    block_number: int
    is_superuser: bool = False
