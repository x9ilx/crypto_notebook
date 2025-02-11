from datetime import date
from enum import Enum

from sqlalchemy import Date
from sqlalchemy import Enum as saEnum
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
	created_at: Mapped[date] = mapped_column(Date)
	risk_minimisation_point: Mapped['RiskMinimisation'] = relationship(
		'RiskMinimisation',
		primaryjoin='RiskMinimisation.transaction_id==Transaction.id',
		lazy='joined',
		cascade='all, delete-orphan',
	)
	currency_id: Mapped[int] = mapped_column(
		Integer, ForeignKey('currency.id'), nullable=False
	)

	def __repr__(self):
		return (
			f'<Transaction(id={self.id}, currency_id={self.currency_id}, '
			f'amount={self.amount}, price={self.price}, '
			f'transaction_type={self.transaction_type}>'
		)
