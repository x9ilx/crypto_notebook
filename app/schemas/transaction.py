from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from schemas.service import RiskMinimisationResponse


class TransactionBase(BaseModel):
	amount: float = Field(gt=0.0)
	price: float = Field(gt=0.0)
	created_at: date


class TransactionCreate(TransactionBase):
	pass


class TransactionUpdate(BaseModel):
	amount: Optional[float] = Field(None, gt=0.0)
	price: Optional[float] = Field(None, gt=0.0)
	created_at: Optional[date] = None


class TransactionResponse(TransactionBase):
	model_config = ConfigDict(from_attributes=True)
	id: int
	currency_id: int
	risk_minimisation_point: Optional[RiskMinimisationResponse]
