from typing import Any, Generic, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import Base
from models.user import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model) -> None:
        self.model = model

    async def _commit_and_refresh(self, obj: ModelType, session: AsyncSession):
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def _add_sorting_field(
        self,
        query,
        field_name: str | None = None,
        field_desc_sort: bool = False,
    ):
        if field_name:
            field = getattr(self.model, field_name, None)
            if field:
                order_desc = field
                if field_desc_sort:
                    order_desc = getattr(field, 'desc')()
                return query.order_by(order_desc)
        return query

    async def _get_by_attribute(
        self, attribute: str, value: str, user: User, session: AsyncSession,
        order_field: str | None = None,
        order_desc: bool = False
    ) -> list[ModelType]:
        attr = getattr(self.model, attribute)
        db_obj = await self._add_sorting_field(
            await session.execute(
                query=select(self.model).where(
                    attr == value, self.model.user_id == user.id
                ),
                field_name=order_field,
                field_desc_sort=order_desc
            )
        )
        return db_obj.scalars().unique().all()

    async def _get_by_attributes(
        self,
        attributes: dict[str, Any],
        query_options: list[Any],
        user: User,
        session: AsyncSession,
        order_field: str | None = None,
        order_desc: bool = False
    ) -> list[ModelType]:
        query = select(self.model)
        query = query.where(self.model.user_id == user.id)
        for attribute, value in attributes.items():
            attr = getattr(self.model, attribute)
            query = query.where(attr == value)
        for option in query_options:
            query = query.options(option)
        result = await session.execute(
            await self._add_sorting_field(
                query=query,
                field_name=order_field,
                field_desc_sort=order_desc
            )
        )
        return result.scalars().unique().all()

    async def _get_first_by_attribute(
        self, attribute: str, value: str, user: User, session: AsyncSession,
        order_field: str | None = None,
        order_desc: bool = False
    ) -> list[ModelType]:
        attr = getattr(self.model, attribute)
        db_obj = await self._add_sorting_field(
            await session.execute(
                query=select(self.model).where(
                    attr == value, self.model.user_id == user.id
                ),
                field_name=order_field,
                field_desc_sort=order_desc
            )
        )
        return db_obj.scalars().first()

    async def get(
        self, obj_id: int, user: User, session: AsyncSession,
        order_field: str | None = None,
        order_desc: bool = False
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            await self._add_sorting_field(
                query=select(self.model).where(
                    self.model.id == obj_id, self.model.user_id == user.id
                ),
                field_name=order_field,
                field_desc_sort=order_desc

            )
        )
        return db_obj.scalars().first()

    async def get_all(
        self,
        user: User,
        session: AsyncSession,
        order_field: str | None = None,
        order_desc: bool = False
    ) -> list[ModelType]:
        db_obj = await session.execute(
            await self._add_sorting_field(
                query=select(self.model).where(
                    self.model.user_id == user.id
                ),
                field_name=order_field,
                field_desc_sort=order_desc
            )
        )
        return db_obj.scalars().unique().all()

    async def create(
        self, obj_in: CreateSchemaType, user: User, session: AsyncSession
    ) -> Optional[ModelType]:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user.id)
        return await self._commit_and_refresh(db_obj, session)

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if update_data[field] == 'null':
                    update_data[field] = None
                setattr(db_obj, field, update_data[field])
        return await self._commit_and_refresh(db_obj, session)

    async def delete(
        self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj
