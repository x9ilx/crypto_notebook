from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_user_is_owner
from models.user import User
from schemas.transaction import TransactionCreate, TransactionType


async def create_transaction(
    currency_id: int,
    new_transaction: TransactionCreate,
    transaction_type: TransactionType,
    user: User,
    session: AsyncSession,
):
    currency = await check_user_is_owner(currency_id, user, session)
    new_transaction._transaction_type = transaction_type
    new_transaction._currency_id = currency.id
    return (currency, new_transaction)
