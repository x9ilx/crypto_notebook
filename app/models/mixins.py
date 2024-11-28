from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


class UserMixin:
    __abstract__ = True
    user_back_populates: str

    user_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('user.id'),
        nullable=False
    )

    @declared_attr
    def user(cls) -> Mapped['models.user.User']:
        return relationship(
            'models.user.User',
            back_populates=cls.user_back_populates
        )
