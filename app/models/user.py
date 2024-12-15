from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from core.db import Base
from models.currency import Currency
from models.services import RiskMinimisation, Service
from models.transaction import Transaction


class User(SQLAlchemyBaseUserTable[int], Base):
    currencies: Mapped[list[Currency]] = relationship(
        Currency, back_populates='user'
    )
    transactions: Mapped[list[Transaction]] = relationship(
        Transaction, back_populates='user'
    )
    risk_minisations: Mapped[list[RiskMinimisation]] = relationship(
        RiskMinimisation, back_populates='user'
    )
    services: Mapped[list[Service]] = relationship(
        Service, back_populates='user'
    )
