from fastapi import APIRouter

from .endpoints import proposal_router, token_router, user_router

__all__ = ["api_router"]

api_router = APIRouter()
api_router.include_router(proposal_router)
api_router.include_router(user_router)
api_router.include_router(token_router, prefix="/token")
