from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.transaction import transaction_crud
from models.currency import Currency
from models.user import User


async def check_transaction_exist(
    transaction_id: int,
    user: User,
    session: AsyncSession,
) -> Optional[Currency]:
    return await check_object_exist(
        object_id=transaction_id,
        crud_class=transaction_crud,
        error_text=f'Транзакции с id {transaction_id} не существует.',
        user=user,
        session=session,
    )