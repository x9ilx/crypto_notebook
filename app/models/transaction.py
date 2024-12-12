from datetime import datetime
from enum import Enum

from core.db import Base
from models.mixins import UserMixin
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class TransactionType(Enum):
    SALE = 'sale'
    PURCHASE = 'purchase'


class Transaction(Base, UserMixin):
    __user_back_populates__ = 'transactions'
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        String, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    risk_minimisations: Mapped[list['RiskMinimisation']] = relationship(
        'RiskMinimisation', back_populates='transaction'
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )
