from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_currency_exist, check_user_is_owner
from core.db import get_async_session
from core.users import current_user
from crud.currency import currency_crud
from models.user import User
from schemas.currency import CurrencyCreate, CurrencyResponse, CurrencyUpdate
from schemas.transaction import (TransactionCreate, TransactionResponse,
                                 TransactionType)

router = APIRouter(prefix='/currency', tags=['Currency'])


@router.get(
    '/',
    response_model=list[CurrencyResponse],
    summary='Позволяет получить все монеты пользователя.',
)
async def currency_get(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[CurrencyResponse]:
    return await currency_crud.get_all(user=user, session=session)


@router.get(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет получить информацию о монете.',
)
async def currency_get(
    currency_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await check_currency_exist(
        currency_id=currency_id, user=user, session=session
    )


@router.post(
    '/',
    response_model=CurrencyResponse,
    summary='Позволяет добавить новую монету в базу.',
    status_code=HTTPStatus.CREATED,
)
async def currency_create(
    currency: CurrencyCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await currency_crud.create(currency, user, session)


@router.patch(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет обновить информацию о монете.',
    description='Для установки пустого значения необходимо отправить null',
)
async def currency_update(
    currency_id: int,
    currency: CurrencyUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await currency_crud.update(
        db_obj=await check_currency_exist(
            currency_id=currency_id, user=user, session=session
        ),
        obj_in=currency,
        session=session,
    )


@router.delete(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет удалить монету из базы.',
)
async def currency_delete(
    currency_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await currency_crud.delete(
        await check_user_is_owner(
            currency_id=currency_id, user=user, session=session
        ),
        session,
    )


@router.post(
    '/{currency_id}/purchases',
    response_model=TransactionResponse,
    summary='Позволяет создать запись о покупке монеты',
)
async def currency_add_purchase(
    currency_id: int,
    purchase: TransactionCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    purchase._transaction_type = TransactionType.PURCHASE
    currency = await check_currency_exist(currency_id, user, session)
    purchase._currency_id = currency.id
    print(purchase)
    return TransactionResponse(
        amount=1,
        price=1.1,
        created_at=datetime.now(),
        currency_id=currency_id,
    )
