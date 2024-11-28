from pydantic import BaseModel, ConfigDict, Field

from models.transaction import Transaction, RiskMinimisation

class CurrencyBase(BaseModel):
    name: str
    description: str | None
    quantity: float = Field(default=0.0, ge=0.0)
    profit: float = Field(default=0.0)


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: str | None
    description: str | None
    quantity: float = Field(None, ge=0.0)
    profit: float | None


class CurrencyResponse(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)
    sales: list[Transaction] = None
    purchases: list[Transaction] = None
    risk_points: list[RiskMinimisation] = None