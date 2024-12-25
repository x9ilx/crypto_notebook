from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_currency_exist
from api.service_validators import check_service_exist
from core.db import get_async_session
from core.users import current_user
from crud.service import service_crud
from models.transaction import TransactionType
from models.user import User
from schemas.service import ServiceCreate, ServiceResponse, ServiceUpdate

router = APIRouter(
    prefix='/currency/{currency_id}/services', tags=['Services']
)


@router.post(
    '/purchase_planning',
    response_model=ServiceResponse,
    summary='Позволяет создать план покупки монеты.',
)
async def currency_add_purchase_plan(
    currency_id: int,
    purchase_plan: ServiceCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await service_crud.create_service(
        currency=await check_currency_exist(
            currency_id=currency_id, user=user, session=session
        ),
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
    currency_id: int,
    sale_plan: ServiceCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await service_crud.create_service(
        currency=await check_currency_exist(
            currency_id=currency_id, user=user, session=session
        ),
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
    currency_id: int,
    service_id: int,
    service_update: ServiceUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_currency_exist(
        currency_id=currency_id, user=user, session=session
    )
    return await service_crud.update(
        db_obj=await check_service_exist(
            service_id=service_id, user=user, session=session
        ),
        obj_in=service_update,
        session=session,
    )


@router.delete(
    '/{service_id}',
    response_model=ServiceResponse,
    summary='Позволяет удалить запись о запланированном действии.',
)
async def transaction_update(
    currency_id: int,
    service_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_currency_exist(
        currency_id=currency_id, user=user, session=session
    )
    return await service_crud.delete(
        db_obj=await check_service_exist(
            service_id=service_id, user=user, session=session
        ),
        session=session,
    )
