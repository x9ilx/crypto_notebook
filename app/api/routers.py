from fastapi import APIRouter

from .endpoints import user_router
from .endpoints import currency_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(currency_router)
