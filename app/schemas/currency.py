from pydantic import BaseModel, ConfigDict, Field

from schemas.transaction import TransactionResponse, RiskMinimisationResponse

class CurrencyBase(BaseModel):
    name: str
    description: str | None
    quantity: float = Field(default=0.0, ge=0.0)


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: str | None
    description: str | None


class CurrencyResponse(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)
    profit: float = Field(default=0.0)
    sales: list[TransactionResponse] = None
    purchases: list[TransactionResponse] = None
    risk_points: list[RiskMinimisationResponse] = None