from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_currency_exist
from api.service_validators import check_service_exist
from core.db import get_async_session
from core.users import current_user
from crud.service import service_crud
from models.currency import Currency
from models.transaction import TransactionType
from models.services import Service
from models.user import User
from schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate

router = APIRouter(
	prefix='/currency/{currency_id}/services', tags=['Services']
)


@router.get(
	'/expected_profit_and_costs',
	response_model=None,
	summary='Позволяет получить ожидаемую прибыль и траты.',
	description=(
     'Сумма инвестиций/изъятия и сумма ожидаемой прибыли/количества монет.'
    ),
	dependencies=[Depends(current_user)]
)
async def get_expected_profit_and_costs(
    service_type: TransactionType,
    currency: Currency = Depends(check_currency_exist),
)-> dict[str, float]:
    return await service_crud.get_amount_investment_and_expected_currency(
        currency=currency,
        service_type=service_type,
	)


@router.post(
	'/purchase_planning',
	response_model=ServiceResponse,
	summary='Позволяет создать план покупки монеты.',
)
async def currency_add_purchase_plan(
	purchase_plan: ServiceCreate,
	currency: Currency = Depends(check_currency_exist),
	user: User = Depends(current_user),
	session: AsyncSession = Depends(get_async_session),
):
	return await service_crud.create_service(
		currency=currency,
		new_service=purchase_plan,
		transaction_type=TransactionType.PURCHASE,
		user=user,
		session=session,
	)


@router.post(
	'/sale_planning',
	response_model=ServiceResponse,
	summary='Позволяет создать план продажи монеты.',
)
async def currency_add_sale_plan(
	sale_plan: ServiceCreate,
	currency: Currency = Depends(check_currency_exist),
	user: User = Depends(current_user),
	session: AsyncSession = Depends(get_async_session),
):
	return await service_crud.create_service(
		currency=currency,
		new_service=sale_plan,
		transaction_type=TransactionType.SALE,
		user=user,
		session=session,
	)


@router.patch(
	'/{service_id}',
	response_model=ServiceResponse,
	summary='Позволяет обновить запись о запланированном действии.',
)
async def transaction_update(
	service_update: ServiceUpdate,
	service: Service = Depends(check_service_exist),
	session: AsyncSession = Depends(get_async_session),
):
	return await service_crud.update(
		db_obj=service,
		obj_in=service_update,
		session=session,
	)


@router.delete(
	'/{service_id}',
	response_model=ServiceResponse,
	summary='Позволяет удалить запись о запланированном действии.',
)
async def transaction_delete(
	service: Service = Depends(check_service_exist),
	session: AsyncSession = Depends(get_async_session),
):
	return await service_crud.delete(
		db_obj=service,
		session=session,
	)
