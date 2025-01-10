from sqlalchemy import CheckConstraint, Enum as saEnum
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

	def __repr__(self):
		return (
			f'<RiskMinimisation(id={self.id}, price={self.price}, '
			f'transaction_id={self.transaction_id}, '
			f'currency_id={self.currency_id}>'
		)


class Service(Base, UserMixin):
	__user_back_populates__ = 'services'
	__table_args__ = (
		CheckConstraint('investments > 0', name='investment_great_than_zero'),
		CheckConstraint('price > 0', name='price_great_than_zero')
	)
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
	currency = relationship('Currency', viewonly=True)

	def __repr__(self):
		return (
			f'<Service(id={self.id}, investments={self.investments}, '
			f'price={self.price}, service_type={self.service_type}, '
			f'currency_id={self.currency_id}>'
		)
