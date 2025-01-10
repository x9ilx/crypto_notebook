from typing import Optional

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
	id: int
	transaction_id: int
	currency_id: int


class ServiceBase(BaseModel):
	investments: float =  Field(..., gt=0.0)
	price: float =  Field(..., gt=0.0)


class ServiceCreate(ServiceBase):
	pass


class ServiceUpdate(BaseModel):
	investments: Optional[float] = Field(None, gt=0.0)
	price: Optional[float] = Field(None, gt=0.0)


class ServiceResponse(ServiceBase):
	model_config = ConfigDict(from_attributes=True)
	id: int
	currency_id: int
