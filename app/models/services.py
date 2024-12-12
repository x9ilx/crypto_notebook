from datetime import datetime
from enum import Enum

from core.db import Base
from models.mixins import UserMixin
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship



class ServiceType(Enum):
    PURCHASE_POINT = 'Purchase point'
    SALE_POINT = 'Sale point'


class RiskMinimisation(Base, UserMixin):
    __user_back_populates__ = 'risk_minisations'
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('transaction.id'), nullable=False
    )
    transaction: Mapped['Transaction'] = relationship(
        'Transaction', back_populates='risk_minimisations'
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )
    currency: Mapped['Currency'] = relationship(
        'Currency', back_populates='risk_points'
    )


class Service(Base, UserMixin):
    __user_back_populates__ = 'services'
    investments: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    service_type: Mapped[ServiceType] = mapped_column(
        String, nullable=False
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('currency.id'), nullable=False
    )