from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_currency_exist
from api.transaction_validators import (
    check_transaction_amount_is_valid_for_sale,
    check_transaction_exist,
)
from core.db import get_async_session
from core.users import current_user
from crud.transaction import transaction_crud
from models.currency import Currency
from models.transaction import Transaction, TransactionType
from models.user import User
from schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)

router = APIRouter(
    prefix='/currency/{currency_id}/transaction', tags=['Transactions']
)


@router.get(
    '/',
    response_model=list[TransactionResponse],
    summary='Позволяет получить все транзакции для валюты.',
    description='Фильтр по типу транзакции, дате',
)
async def transaction_get_all(
    currency_id: int,
    transaction_type_filter: TransactionType | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[TransactionResponse]:
    pass


@router.get(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Позволяет получить информацию о транзакции.',
)
async def transaction_get(
    transaction: Transaction = Depends(check_transaction_exist),
) -> TransactionResponse:
    return transaction


@router.post(
    '/purchases',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о покупке монеты.',
)
async def currency_add_purchase(
    purchase: TransactionCreate,
    currency: Currency = Depends(check_currency_exist),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    currency.quantity += purchase.amount
    return await transaction_crud.create_transaction(
        currency=currency,
        new_transaction=purchase,
        transaction_type=TransactionType.PURCHASE,
        user=user,
        session=session,
    )


@router.post(
    '/sales',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о продаже монеты.',
)
async def currency_add_sale(
    sale: TransactionCreate,
    currency: Currency = Depends(check_currency_exist),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    currency.quantity -= sale.amount
    await check_transaction_amount_is_valid_for_sale(
        currency=currency, amount=sale.amount
    )
    return await transaction_crud.create_transaction(
        currency=currency,
        new_transaction=sale,
        transaction_type=TransactionType.SALE,
        user=user,
        session=session,
    )


@router.patch(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Позволяет обновить запись о транзакции.',
)
async def transaction_update(
    transaction_update: TransactionUpdate,
    transaction: Transaction = Depends(check_transaction_exist),
    session: AsyncSession = Depends(get_async_session),
):
    return await transaction_crud.update_transaction(
        transaction=transaction,
        updated_transaction=transaction_update,
        session=session,
    )


@router.delete(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Позволяет удалить запись о транзакции.',
)
async def transaction_delete(
    transaction: Transaction = Depends(check_transaction_exist),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await transaction_crud.delete(
        db_obj=transaction,
        session=session,
    )
