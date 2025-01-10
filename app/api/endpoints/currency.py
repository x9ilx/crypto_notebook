from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import (
	check_currency_exist,
	check_currency_name_is_unique,
)
from core.db import get_async_session
from core.users import current_user
from crud.currency import currency_crud
from models.currency import Currency
from models.user import User
from schemas.currency import CurrencyCreate, CurrencyResponse, CurrencyUpdate


router = APIRouter(prefix='/currency', tags=['Currency'])


@router.get(
	'/',
	response_model=list[CurrencyResponse],
	summary='Позволяет получить все монеты пользователя.',
)
async def currency_get_all(
	name: str | None = None,
	order_field: str | None = 'name',
	order_desc: bool = False,
	user: User = Depends(current_user),
	session: AsyncSession = Depends(get_async_session),
) -> list[CurrencyResponse]:
	return await currency_crud.get_all_with_name_filter(
		name=name,
		user=user,
		session=session,
		order_field=order_field,
		order_desc=order_desc,
	)


@router.get(
	'/{currency_id}',
	response_model=CurrencyResponse,
	summary='Позволяет получить информацию о монете.',
)
async def currency_get(
	currency: Currency = Depends(check_currency_exist),
) -> CurrencyResponse:
	return currency


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
	await check_currency_name_is_unique(
		name=currency.name,
		user=user,
		session=session,
	)
	return await currency_crud.create(currency, user, session)


@router.patch(
	'/{currency_id}',
	response_model=CurrencyResponse,
	summary='Позволяет обновить информацию о монете.',
	description='Для установки пустого значения необходимо отправить null',
)
async def currency_update(
	new_currency: CurrencyUpdate,
	existing_currency: Currency = Depends(check_currency_exist),
	session: AsyncSession = Depends(get_async_session),
):
	return await currency_crud.update(
		db_obj=existing_currency,
		obj_in=new_currency,
		session=session,
	)


@router.delete(
	'/{currency_id}',
	response_model=CurrencyResponse,
	summary='Позволяет удалить монету из базы.',
)
async def currency_delete(
	currency: Currency = Depends(check_currency_exist),
	session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
	return await currency_crud.delete(currency, session)
