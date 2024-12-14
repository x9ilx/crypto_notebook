from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.currency import currency_crud
from models.currency import Currency
from models.user import User


async def check_currency_exist(
    currency_id: int,
    user: User,
    session: AsyncSession,
) -> Optional[Currency]:
    return await check_object_exist(
        object_id=currency_id,
        crud_class=currency_crud,
        error_text=f'Монеты с id {currency_id} не существует.',
        user=user,
        session=session,
    )


async def check_user_is_owner(
    currency_id: int, user: User, session: AsyncSession
):
    currency: Currency = await check_currency_exist(
        currency_id=currency_id, user=user, session=session
    )
    if currency.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Только владелец монеты может её удалить',
        )
    return currency
