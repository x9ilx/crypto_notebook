from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, relationship

from core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    currencies: Mapped['Currency'] = relationship(
        'Currency', back_populates='user'
    )
    transactions: Mapped['Transaction'] = relationship(
        'Transaction', back_populates='user'
    )
    risk_minisations: Mapped['RiskMinimisation'] = relationship(
        'RiskMinimisation', back_populates='user'
    )
