from fastapi import APIRouter
from starlette import status

import schemas
import services

api_router = APIRouter(prefix="/api/v1")


@api_router.get(
    "/balance/{address}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.GetBalance,
)
def get_balance_by_address(address: str) -> dict:
    return services.get_balance_by_address(address)


@api_router.get(
    "/info/latest_block",
    status_code=status.HTTP_200_OK,
    response_model=schemas.GetInfoByBlock,
)
def get_info_by_latest_block():
    return services.get_info_by_latest_block()


@api_router.get(
    "/verify_address/{address}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.GetVerify,
)
def verify_address(address: str):
    return services.verify_address(address)
