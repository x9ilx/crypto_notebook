from fastapi import APIRouter

from .endpoints import (
    currency_router,
    service_router,
    transaction_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(currency_router)
main_router.include_router(service_router)
main_router.include_router(transaction_router)
