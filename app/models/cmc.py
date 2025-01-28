from datetime import date

from sqlalchemy import BigInteger, Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class CMCData(Base):
    cmc_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)
    cmc_rank: Mapped[int] = mapped_column(Integer)
    circulating_supply: Mapped[int] = mapped_column(BigInteger)
    total_supply: Mapped[int] = mapped_column(BigInteger)
    last_updated: Mapped[date] = Mapped[Date]
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    percent_change_24h: Mapped[float] = mapped_column(Float)
    percent_change_7d: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return (
            f'<Currency(id={self.id}, name={self.name}, '
            f'description={self.description}, quantity={self.quantity}, '
            f'profit={self.profit}; user={self.user}>'
        )
