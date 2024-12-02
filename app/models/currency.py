from typing import Optional

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.mixins import UserMixin


class Currency(Base, UserMixin):
    lazy='selectin' 
    __user_back_populates__ = 'currencies'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    sales: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='currency',
        primaryjoin=(
            'and_(Transaction.currency_id==Currency.id, '
            'Transaction.transaction_type=="sale")'
        ),
        overlaps='purchases'
    )
    purchases: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='currency',
        primaryjoin=(
            'and_(Transaction.currency_id==Currency.id, '
            'Transaction.transaction_type=="purchase")'
        ),
        overlaps='sales'
    )
    risk_points: Mapped[list['RiskMinimisation']] = relationship(
        'RiskMinimisation', back_populates='currency'
    )

    def __repr__(self):
        return (
            f'<Currency(id={self.id}, name='
            f'{self.name}, description={self.description}'
        )
