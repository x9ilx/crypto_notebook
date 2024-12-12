from typing import Optional

from core.db import Base
from models.mixins import UserMixin
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Currency(Base, UserMixin):
    lazy = 'selectin'
    __user_back_populates__ = 'currencies'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    profit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sales: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='currency',
        primaryjoin=(
            'and_(Transaction.currency_id==Currency.id, '
            'Transaction.transaction_type=="sale")'
        ),
        overlaps='purchases',
        lazy='joined',
    )
    purchases: Mapped[list['Transaction']] = relationship(
        'Transaction',
        back_populates='currency',
        primaryjoin=(
            'and_(Transaction.currency_id==Currency.id, '
            'Transaction.transaction_type=="purchase")'
        ),
        overlaps='sales',
        lazy='joined',
    )
    risk_points: Mapped[list['RiskMinimisation']] = relationship(
        'RiskMinimisation', back_populates='currency', lazy='joined'
    )

    def __repr__(self):
        return (
            f'<Currency(id={self.id}, name='
            f'{self.name}, description={self.description}, '
            f'quantity={self.quantity}, profit={self.profit}; '
            f'sales={self.sales} purchases={self.purchases} '
            f'risk_points={self.risk_points}, user={self.user}>'
            
        )
