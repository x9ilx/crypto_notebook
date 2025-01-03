from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.base_validators import check_object_exist
from crud.transaction import transaction_crud
from models.currency import Currency
from models.transaction import Transaction, TransactionType
from models.user import User


async def check_transaction_exist(
    transaction_id: int,
    user: User,
    session: AsyncSession,
) -> Optional[Transaction]:
    return await check_object_exist(
        object_id=transaction_id,
        crud_class=transaction_crud,
        error_text=f'Транзакции с id {transaction_id} не существует.',
        user=user,
        session=session,
    )


async def check_transaction_amount_is_valid_for_sale(
    currency: Currency, amount: float
) -> None:
    if currency.quantity - amount < 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Невозможно продать больше монет, чем есть в наличии.',
        )
