from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as saEnum
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.db import Base
from models.mixins import UserMixin


class TransactionType(Enum):
    SALE = 'SALE'
    PURCHASE = 'PURCHASE'


class Transaction(Base, UserMixin):
    __user_back_populates__ = 'transactions'
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        saEnum(
            TransactionType, name='transactiontype', create_constraint=True
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    risk_minimisation_point: Mapped['RiskMinimisation'] = relationship(
        'RiskMinimisation',
        primaryjoin='RiskMinimisation.transaction_id==Transaction.id',
        lazy='joined',
        cascade='all, delete',
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )
