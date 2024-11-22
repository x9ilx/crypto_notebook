from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Float, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class TransactionType(Enum):
    SALE = "sale"
    PURCHASE = "purchase"


class Transaction(Base):
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[TransactionType]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    risk_minimisations: Mapped[list['RiskMinimisation']] = relationship(
        'RiskMinimisation',
        back_populates='transaction'
    )
    currency_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('currency.id'),
        nullable=False
    )
    currency: Mapped['Currency'] = relationship(
        'Currency',
        back_populates='sales'
    )


class RiskMinimisation(Base):
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('transaction.id'),
        nullable=False
    )
    transaction: Mapped['Transaction'] = relationship(
        'Transaction',
        back_populates='risk_minimisations'
    )
    currency_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('currency.id'),
        nullable=False
    )
    currency: Mapped['Currency'] = relationship(
        'Currency',
        back_populates='sales'
    )