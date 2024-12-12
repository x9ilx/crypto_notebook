from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.transaction import TransactionType
from schemas.service import RiskMinimisationResponse


class TransactionBase(BaseModel):
    transaction_type: TransactionType
    amount: float
    price: float


class TransactionCreate(TransactionBase):
    currency_id: int


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    price: Optional[float] = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    currency_id: int
    risk_minimisations: list[RiskMinimisationResponse] = None
