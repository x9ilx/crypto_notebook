from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.service import service_crud
from models.services import Service
from models.user import User


async def check_service_exist(
    service_id: int,
    user: User,
    session: AsyncSession,
) -> Optional[Service]:
    return await check_object_exist(
        object_id=service_id,
        crud_class=service_crud,
        error_text=f'Плана с id {service_id} не существует.',
        user=user,
        session=session,
    )
