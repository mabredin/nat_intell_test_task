from fastapi import APIRouter

from .endpoints import proposal_router

__all__ = ["api_router"]

api_router = APIRouter()
api_router.include_router(proposal_router, prefix="/proposal")