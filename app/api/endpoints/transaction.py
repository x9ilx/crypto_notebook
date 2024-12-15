from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_service import create_transaction
from api.currency_validators import check_user_is_owner
from api.transaction_validators import check_transaction_exist
from core.db import get_async_session
from core.users import current_user
from crud.transaction import transaction_crud
from models.user import User
from schemas.transaction import (TransactionCreate, TransactionResponse,
                                 TransactionType, TransactionUpdate)

router = APIRouter(
    prefix='/currency/{currency_id}/transaction', tags=['Transactions']
)


@router.post(
    '/purchases',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о покупке монеты.',
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
    summary='Позволяет создать запись о продаже монеты.',
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


@router.patch(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Позволяет обновить запись о покупке монеты.',
)
async def transaction_update(
    currency_id: int,
    transaction_id: int,
    transaction_update: TransactionUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_user_is_owner(
        currency_id=currency_id,
        user=user,
        session=session
    )
    return await transaction_crud.update_transaction(
        transaction=await check_transaction_exist(
            transaction_id=transaction_id,
            user=user,
            session=session
        ),
        updated_transaction=transaction_update,
        session=session
    )


@router.delete(
    '/{transaction_id}',
    response_model=TransactionResponse,
    summary='Позволяет удалить запись о покупке монеты.',
)
async def transaction_update(
    currency_id: int,
    transaction_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_user_is_owner(
        currency_id=currency_id,
        user=user,
        session=session
    )
    return await transaction_crud.delete(
        db_obj=await check_transaction_exist(
            transaction_id=transaction_id,
            user=user,
            session=session
        ),
        session=session
    )