from typing import Optional

from pydantic import BaseModel, ConfigDict


class RiskMinimisationBase(BaseModel):
    price: float


class RiskMinimisationCreate(RiskMinimisationBase):
    currency_id: int
    transaction_id: int


class RiskMinimisationUpdate(RiskMinimisationBase):
    pass


class RiskMinimisationResponse(RiskMinimisationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    transaction_id: int
    currency_id: int


class ServiceBase(BaseModel):
    investments: float
    price: float


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    investments: Optional[float] = None
    price: Optional[float] = None


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    currency_id: int
