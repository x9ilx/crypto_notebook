from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.currency import Currency
from models.user import User
from schemas.currency import CurrencyCreate, CurrencyUpdate


class CRUDCurrency(CRUDBase[Currency, CurrencyCreate, CurrencyUpdate]):
    def __init__(self) -> None:
        super().__init__(Currency)

    async def get_all_with_name_filter(
        self,
        user: User,
        session: AsyncSession,
        name: str| None = None,
    ) -> list[Currency]:
        if not name:
            return await self.get_all(user=user, session=session)
        result = await session.execute(
            select(Currency)
            .where(
                Currency.name.startswith(name.upper()),
                Currency.user_id == user.id,
            )
        )
        return result.scalars().unique().all()

currency_crud = CRUDCurrency()
