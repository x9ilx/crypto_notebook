from fastapi import APIRouter

from frontend.endpoints import (
    frontend_base,
    frontend_currency_router,
)

frontend_router = APIRouter()
frontend_router.include_router(frontend_base)
frontend_router.include_router(frontend_currency_router)
