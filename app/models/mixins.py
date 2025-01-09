from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship


class UserMixin:
	__abstract__ = True
	__user_back_populates__: str

	user_id: Mapped[int] = mapped_column(
		Integer, ForeignKey('user.id'), nullable=False
	)

	@declared_attr
	def user(cls) -> Mapped['models.user.User']:
		return relationship(
			'models.user.User',
			back_populates=cls.__user_back_populates__,
			lazy='joined',
		)
