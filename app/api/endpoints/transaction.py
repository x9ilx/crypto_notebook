from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_service import create_transaction
from core.db import get_async_session
from core.users import current_user
from crud.transaction import transaction_crud
from models.user import User
from schemas.transaction import (TransactionCreate, TransactionResponse,
                                 TransactionType)

router = APIRouter(
    prefix='/currency/{currency_id}/transaction', tags=['Transactions']
)


@router.post(
    '/purchases',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о покупке монеты',
)
async def currency_add_purchase(
    currency_id: int,
    purchase: TransactionCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    currency, purchase = await create_transaction(
        currency_id=currency_id,
        new_transaction=purchase,
        transaction_type=TransactionType.PURCHASE,
        user=user,
        session=session,
    )
    return await transaction_crud.create_transaction(
        currency=currency, new_transaction=purchase, user=user, session=session
    )


@router.post(
    '/sales',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о продаже монеты',
)
async def currency_add_sale(
    currency_id: int,
    sale: TransactionCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    currency, sale = await create_transaction(
        currency_id=currency_id,
        new_transaction=sale,
        transaction_type=TransactionType.SALE,
        user=user,
        session=session,
    )
    return await transaction_crud.create_transaction(
        currency=currency, new_transaction=sale, user=user, session=session
    )
