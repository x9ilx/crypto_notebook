from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.currency import Currency
from models.services import RiskMinimisation
from models.transaction import Transaction, TransactionType
from models.user import User
from schemas.transaction import TransactionCreate, TransactionUpdate

RISK_MINIMAISATION_MULTIPLER = 2


class CRUDTransaction(
    CRUDBase[Transaction, TransactionCreate, TransactionUpdate]
):
    def __init__(self) -> None:
        super().__init__(Transaction)

    async def create_transaction(
        self,
        currency: Currency,
        new_transaction: TransactionCreate,
        transaction_type: TransactionType,
        user: User,
        session: AsyncSession,
    ):
        transaction: Transaction = Transaction(
            amount=new_transaction.amount,
            price=new_transaction.price,
            transaction_type=transaction_type,
            currency_id=currency.id,
            created_at=new_transaction.created_at,
            user_id=user.id,
        )
        currency.purchases.append(transaction)
        new_obj = await self._commit_and_refresh(
            obj=transaction, session=session
        )
        if transaction_type == TransactionType.PURCHASE:
            risk_minimisation = RiskMinimisation(
                price=new_obj.price * RISK_MINIMAISATION_MULTIPLER,
                transaction_id=new_obj.id,
                currency_id=new_obj.currency_id,
                user_id=new_obj.user_id,
            )
            new_obj.risk_minimisation_point = risk_minimisation
        return await self._commit_and_refresh(obj=new_obj, session=session)

    async def update_transaction(
        self,
        transaction: Transaction,
        updated_transaction: TransactionUpdate,
        session: AsyncSession,
    ):
        if (
            transaction.transaction_type == TransactionType.PURCHASE
            and updated_transaction.price
        ):
            transaction.risk_minimisation_point.price = (
                updated_transaction.price * RISK_MINIMAISATION_MULTIPLER
            )
        return await super().update(
            db_obj=transaction, obj_in=updated_transaction, session=session
        )


transaction_crud = CRUDTransaction()
