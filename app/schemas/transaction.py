from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from models.transaction import TransactionType
from schemas.service import RiskMinimisationResponse


class TransactionBase(BaseModel):
    _transaction_type: TransactionType = PrivateAttr(
        default=TransactionType.PURCHASE
    )
    amount: float
    price: float


class TransactionCreate(TransactionBase):
    _currency_id: int
    _user_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    price: Optional[float] = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    currency_id: int
    risk_minimisation_point: Optional[RiskMinimisationResponse]
