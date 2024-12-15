from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from models.transaction import TransactionType


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


class ServiceBase(BaseModel):
    service_type: TransactionType
    investments: float
    price: float


class ServiceCreate(ServiceBase):
    currency_id: int


class ServiceUpdate(BaseModel):
    investments: Optional[float] = None
    price: Optional[float] = None


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    currency_id: int
