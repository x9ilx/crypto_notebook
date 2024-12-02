from crud.base import CRUDBase
from models.transaction import RiskMinimisation, Transaction
from schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    RiskMinimisationCreate,
    RiskMinimisationUpdate
)


class CRUDRiskMinimisation(
    CRUDBase[RiskMinimisation, RiskMinimisationCreate, RiskMinimisationUpdate]
):
    def __init__(self) -> None:
        super().__init__(RiskMinimisation)


class CRUDTransaction(
    CRUDBase[Transaction, TransactionCreate, TransactionUpdate]
):
    def __init__(self) -> None:
        super().__init__(Transaction)


transaction_crud = CRUDTransaction()
risk_minimisation_crud = CRUDRiskMinimisation()