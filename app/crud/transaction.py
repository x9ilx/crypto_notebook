from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.currency import Currency
from models.services import RiskMinimisation
from models.transaction import Transaction, TransactionType
from models.user import User
from schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDTransaction(
    CRUDBase[Transaction, TransactionCreate, TransactionUpdate]
):
    def __init__(self) -> None:
        super().__init__(Transaction)

    async def create_transaction(
        self,
        currency: Currency,
        new_transaction: TransactionCreate,
        user: User,
        session: AsyncSession,
    ):
        transaction: Transaction = Transaction(
            amount=new_transaction.amount,
            price=new_transaction.price,
            transaction_type=new_transaction._transaction_type,
            currency_id=new_transaction._currency_id,
            created_at=datetime.now(),
            user_id=user.id,
        )
        currency.purchases.append(transaction)
        new_obj = await self._commit_and_refresh(
            obj=transaction, session=session
        )
        if new_transaction._transaction_type == TransactionType.PURCHASE:
            risk_minimisation = RiskMinimisation(
                price=new_obj.price * 2,
                transaction_id=new_obj.id,
                currency_id=new_obj.currency_id,
                user_id=new_obj.user_id,
            )
            new_obj.risk_minimisation_point = await self._commit_and_refresh(
                obj=risk_minimisation, session=session
            )
        return new_obj


transaction_crud = CRUDTransaction()
