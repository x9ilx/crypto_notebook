import operator
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
  		order_by='desc(Transaction.created_at)',
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
  		order_by='desc(Transaction.created_at)',
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
        order_by='Service.price',
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
        order_by='desc(Service.price)',
	)

	def __get_services_statictic_data(
		self,
		service_type: TransactionType
	) -> dict[str, float]:
		if service_type == TransactionType.PURCHASE:
			operation = operator.truediv
			service_list = self.service_purchases_points
		else:
			operation = operator.mul
			service_list = self.service_sales_points
		element_count = len(service_list)
		result = {
			'total_investments': 0,
			'total_profit': 0,
			'avg_price': 0,
		}
		for service in service_list:
			result['total_investments'] += service.investments
			result['total_profit'] += operation(
				service.investments,
				service.price
			)
			result['avg_price'] += service.price / element_count
		return result

	def __get_transactions_statictic_data(
		self,
		transaction_type: TransactionType
	) -> dict[str, float]:
		transaction_list = (
			self.purchases
			if transaction_type == TransactionType.PURCHASE
			else self.sales
		)
		transaction_count = len(transaction_list)
		result = {
			'total_amount': 0,
			'total_cost': 0,
			'avg_risk_minimisation_point': 0,
			'avg_price': 0,
		}
		for transaction in transaction_list:
			result['total_amount'] += transaction.amount
			result['total_cost'] += transaction.amount * transaction.price
			if transaction.risk_minimisation_point:
				result['avg_risk_minimisation_point'] += (
					transaction.risk_minimisation_point.price
     				/ transaction_count
				)
			result['avg_price'] += transaction.price / transaction_count
		return result

	@property
	def get_purchase_plan_statistics(
    	self
    ) -> dict[str, float]:
		return self.__get_services_statictic_data(
			service_type=TransactionType.PURCHASE
		)

	@property
	def get_sale_plan_statistics(
    	self
    ) -> dict[str, float]:
		return self.__get_services_statictic_data(
			service_type=TransactionType.SALE
		)

	@property
	def get_purchase_statistics(
    	self
    ) -> dict[str, float]:
		return self.__get_transactions_statictic_data(
			transaction_type=TransactionType.PURCHASE
		)

	@property
	def get_sale_statistics(
    	self
    ) -> dict[str, float]:
		return self.__get_transactions_statictic_data(
			transaction_type=TransactionType.SALE
		)

	def __repr__(self):
		return (
			f'<Currency(id={self.id}, name={self.name}, '
			f'description={self.description}, quantity={self.quantity}, '
			f'profit={self.profit}; user={self.user}>'
		)
