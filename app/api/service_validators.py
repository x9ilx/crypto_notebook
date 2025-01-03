from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from api.currency_validators import check_currency_exist
from core.db import get_async_session
from core.users import current_user
from crud.service import service_crud
from models.services import Service
from models.user import User


async def check_service_exist(
    currency_id: int,
    service_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[Service]:
    await check_currency_exist(
        currency_id=currency_id,
        user=user,
        session=session
    )
    return await check_object_exist(
        object_id=service_id,
        crud_class=service_crud,
        error_text=f'Плана с id {service_id} не существует.',
        user=user,
        session=session,
    )
