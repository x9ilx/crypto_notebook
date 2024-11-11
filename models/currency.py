from core.db import Base
from sqlalchemy import Column, Float, String


class Currency(Base):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    quantity = Column(Float, nullable=False, default=0.0)
    profit = Column(Float, nullable=False)

    def __repr__(self):
        return (
            f"<Currency(id={self.id}, name="
            f"{self.name}, description={self.description}"
        )
