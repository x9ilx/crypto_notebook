from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from core.db import get_async_session
from core.users import current_user
from crud.currency import currency_crud
from models.currency import Currency
from models.user import User


async def check_currency_exist(
    currency_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[Currency]:
    return await check_object_exist(
        object_id=currency_id,
        crud_class=currency_crud,
        error_text=(
            f'Монеты с id {currency_id} не существует у текущего пользователя.'
        ),
        user=user,
        session=session,
    )


async def check_currency_name_is_unique(
    name: str,
    session
)->bool:
    pass