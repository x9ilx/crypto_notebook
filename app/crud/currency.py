from crud.base import CRUDBase
from models.currency import Currency
from schemas.currency import CurrencyCreate, CurrencyUpdate


class CRUDCurrency(CRUDBase[Currency, CurrencyCreate, CurrencyUpdate]):
    def __init__(self) -> None:
        super().__init__(Currency)


currency_crud = CRUDCurrency()
