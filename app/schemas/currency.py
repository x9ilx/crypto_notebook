import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from schemas.transaction import RiskMinimisationResponse, TransactionResponse


class CurrencyBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    quantity: float = Field(default=0.0, ge=0.0)

    @field_validator('name')
    @classmethod
    def correct_name(cls, value: str) -> str:
        if not re.compile(r'^[a-zA-Z0-9]*$').match(value):
            raise ValueError(
                'Название монеты может содержать только цифры и латинские буквы'
            )
        return value.upper()


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CurrencyResponse(CurrencyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    profit: float = Field(default=0.0)
    sales: list[TransactionResponse] = []
    purchases: list[TransactionResponse] = []
    risk_points: list[RiskMinimisationResponse] = []
