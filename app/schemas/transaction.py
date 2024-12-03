from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RiskMinimisationBase(BaseModel):
    price: float


class RiskMinimisationCreate(RiskMinimisationBase):
    currency_id: int
    transaction_id: int


class RiskMinimisationUpdate(RiskMinimisationBase):
    pass


class RiskMinimisationResponse(RiskMinimisationBase):
    model_config = ConfigDict(from_attributes=True)
    transaction_id: int
    currency_id: int


class TransactionBase(BaseModel):
    amount: float
    price: float


class TransactionCreate(TransactionBase):
    currency_id: int


class TransactionUpdate(BaseModel):
    amount: float | None
    price: float | None


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    currency_id: int
    risk_minimisations: list[RiskMinimisationResponse] = None