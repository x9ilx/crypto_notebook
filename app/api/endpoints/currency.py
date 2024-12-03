from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.users import current_user
from crud.currency import currency_crud
from models.currency import Currency
from models.user import User
from schemas.currency import CurrencyCreate, CurrencyResponse


router = APIRouter(
    prefix='/currency',
    tags=['currency']
)


@router.post(
    '/',
    response_model=CurrencyResponse,
    summary='Позволяет добавить новую монету в базу.'
)
def currency_create(
    currency: CurrencyCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
) -> CurrencyResponse:
    pass