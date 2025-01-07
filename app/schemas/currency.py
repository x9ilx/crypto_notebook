import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.service import RiskMinimisationResponse, ServiceResponse
from schemas.transaction import TransactionResponse


class NameValidator:
    @field_validator('name')
    @classmethod
    def correct_name(cls, value: str) -> str:
        if not re.compile(r'^[a-zA-Z0-9]*$').match(value):
            raise ValueError(
                'Название монеты может содержать только цифры и латинские буквы'
            )
        return value.upper()


class CurrencyBase(BaseModel, NameValidator):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    quantity: float = Field(default=0.0, ge=0.0)


class CurrencyCreate(CurrencyBase, NameValidator):
    pass


class CurrencyUpdate(BaseModel, NameValidator):
    name: Optional[str] = None
    description: Optional[str] = None


class CurrencyResponse(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    profit: float = Field(default=0.0)
    sales: list[TransactionResponse] = []
    purchases: list[TransactionResponse] = []
    risk_minimisation_points: list[RiskMinimisationResponse] = []
    service_sales_points: list[ServiceResponse] = []
    service_purchases_points: list[ServiceResponse] = []
