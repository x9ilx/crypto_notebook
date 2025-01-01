from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.service import RiskMinimisationResponse


class TransactionBase(BaseModel):
    amount: float = Field(gt=0.0)
    price: float = Field(gt=0.0)
    create_at: datetime


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0.0)
    price: Optional[float] = Field(None, gt=0.0)
    create_at: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    currency_id: int
    risk_minimisation_point: Optional[RiskMinimisationResponse]
