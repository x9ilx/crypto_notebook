from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


class UserMixin:
    __abstract__ = True
    __user_back_populates__: str

    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('user.id'),
        nullable=False
    )

    @declared_attr
    def user(cls) -> Mapped['models.user.User']:
        return relationship(
            'models.user.User',
            back_populates=cls.__user_back_populates__
        )
