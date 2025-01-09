from typing import Optional

from sqlalchemy import Float, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from models.mixins import UserMixin
from models.transaction import TransactionType


class Currency(Base, UserMixin):
	__table_args__ = (
		UniqueConstraint('name', 'user_id', name='name_user_id_unique'),
	)
	lazy = 'selectin'
	__user_back_populates__ = 'currencies'
	name: Mapped[str] = mapped_column(String, nullable=False)
	description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
	quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
	profit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
	image_path: Mapped[str] = mapped_column(
		String, nullable=True, default=None
	)
	current_price: Mapped[float] = mapped_column(
		Float, nullable=False, default=0.0
	)
	sales: Mapped[list['Transaction']] = relationship(
		'Transaction',
		primaryjoin=(
			f'and_(Transaction.currency_id==Currency.id, '
			f'Transaction.transaction_type=="{TransactionType.SALE.name}")'
		),
		overlaps='purchases',
		lazy='joined',
		cascade='all, delete-orphan',
	)
	purchases: Mapped[list['Transaction']] = relationship(
		'Transaction',
		primaryjoin=(
			f'and_(Transaction.currency_id==Currency.id, '
			f'Transaction.transaction_type=="{TransactionType.PURCHASE.name}")'
		),
		overlaps='sales',
		lazy='joined',
		cascade='all, delete-orphan',
	)
	risk_minimisation_points: Mapped[list['RiskMinimisation']] = relationship(
		'RiskMinimisation', lazy='joined', cascade='all, delete-orphan'
	)
	service_sales_points: Mapped[list['Service']] = relationship(
		'Service',
		primaryjoin=(
			f'and_(Service.currency_id==Currency.id, '
			f'Service.service_type=="{TransactionType.SALE.name}")'
		),
		overlaps='service_purchases_points',
		lazy='joined',
		cascade='all, delete-orphan',
	)
	service_purchases_points: Mapped[list['Service']] = relationship(
		'Service',
		primaryjoin=(
			f'and_(Service.currency_id==Currency.id, '
			f'Service.service_type=="{TransactionType.PURCHASE.name}")'
		),
		overlaps='service_sales_points',
		lazy='joined',
		cascade='all, delete-orphan',
	)

	def __repr__(self):
		return (
			f'<Currency(id={self.id}, name={self.name}, '
			f'description={self.description}, quantity={self.quantity}, '
			f'profit={self.profit}; user={self.user}>'
		)
