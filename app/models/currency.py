from typing import Optional

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.mixins import UserMixin
from models.transaction import TransactionType


class Currency(Base, UserMixin):
    lazy = 'selectin'
    __user_back_populates__ = 'currencies'
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    profit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    sales: Mapped[list['Transaction']] = relationship(
        'Transaction',
        primaryjoin=(
            f'and_(Transaction.currency_id==Currency.id, '
            f'Transaction.transaction_type=="{TransactionType.SALE.name}")'
        ),
        overlaps='purchases',
        lazy='joined',
    )
    purchases: Mapped[list['Transaction']] = relationship(
        'Transaction',
        primaryjoin=(
            f'and_(Transaction.currency_id==Currency.id, '
            f'Transaction.transaction_type=="{TransactionType.PURCHASE.name}")'
        ),
        overlaps='sales',
        lazy='joined',
        cascade='all, delete',
    )
    risk_minimisation_points: Mapped[list['RiskMinimisation']] = relationship(
        'RiskMinimisation',
        primaryjoin='RiskMinimisation.currency_id==Currency.id',
        lazy='joined',
    )
    service_sales_points: Mapped[list['Service']] = relationship(
        'Service',
        primaryjoin=(
            f'and_(Service.currency_id==Currency.id, '
            f'Service.service_type=="{TransactionType.SALE.name}")'
        ),
        overlaps='service_purchases_points',
        lazy='joined',
        cascade='all, delete',
    )
    service_purchases_points: Mapped[list['Service']] = relationship(
        'Service',
        primaryjoin=(
            f'and_(Service.currency_id==Currency.id, '
            f'Service.service_type=="{TransactionType.PURCHASE.name}")'
        ),
        overlaps='service_sales_points',
        lazy='joined',
        cascade='all, delete',
    )

    def __repr__(self):
        return (
            f'<Currency(id={self.id}, name='
            f'{self.name}, description={self.description}, '
            f'quantity={self.quantity}, profit={self.profit}; '
            f'sales={self.sales} purchases={self.purchases} '
            f'risk_points={self.risk_points}, user={self.user}>'
        )
