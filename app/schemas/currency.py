from pydantic import BaseModel, ConfigDict, Field, field_validator
from schemas.transaction import RiskMinimisationResponse, TransactionResponse


class CurrencyBase(BaseModel):
    name: str = Field(..., min_length=1, pattern=r'^[a-zA-Z0-9 _]*$')
    description: str | None
    quantity: float = Field(default=0.0, ge=0.0)

    @field_validator('name')
    def correct_name(cls, value: str):
        if '$' in value:
            raise ValueError('Введите название монеты без `$`')
        return value.upper()


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    name: str | None
    description: str | None


class CurrencyResponse(CurrencyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
    profit: float = Field(default=0.0)
    sales: list[TransactionResponse] = []
    purchases: list[TransactionResponse] = []
    risk_points: list[RiskMinimisationResponse] = []
