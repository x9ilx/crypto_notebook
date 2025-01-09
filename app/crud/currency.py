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
        order_field: str | None = None,
        order_desc: bool = False,
    ) -> list[Currency]:
        if not name:
            return await self.get_all(
                user=user,
                session=session,
                order_field=order_field,
                order_desc=order_desc,
            )
        result = await self._add_sorting_field(
            query=await session.execute(
                select(Currency)
                .where(
                    Currency.name.startswith(name.upper()),
                    Currency.user_id == user.id,
                )
            ),
            field_name=order_field,
            field_desc_sort=order_desc,
        )
        return result.scalars().unique().all()

currency_crud = CRUDCurrency()
