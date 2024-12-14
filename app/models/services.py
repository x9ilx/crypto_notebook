from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as saEnum
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.mixins import UserMixin
from models.transaction import TransactionType


class RiskMinimisation(Base, UserMixin):
    __user_back_populates__ = 'risk_minisations'
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('transaction.id'), nullable=False
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )


class Service(Base, UserMixin):
    __user_back_populates__ = 'services'
    investments: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    service_type: Mapped[TransactionType] = mapped_column(
        saEnum(
            TransactionType, name='transactiontype', create_constraint=True
        ),
        nullable=False,
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )
