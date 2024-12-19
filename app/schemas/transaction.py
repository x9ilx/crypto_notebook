from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.service import RiskMinimisationResponse


class TransactionBase(BaseModel):
    amount: float
    price: float


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    price: Optional[float] = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    currency_id: int
    risk_minimisation_point: Optional[RiskMinimisationResponse]
