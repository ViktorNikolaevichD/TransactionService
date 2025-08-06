from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import asc, delete, desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import Base
from utils import with_session

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def add_one(self, data: dict, *args, **kwargs) -> T: ...

    @abstractmethod
    async def find_one(
        self, order_by: Optional[list[tuple[str, str]]], *args, **filter_by
    ) -> Optional[T]: ...

    @abstractmethod
    async def find_all(self, *args, **filter_by) -> Sequence[T]: ...

    @abstractmethod
    async def update_one(self, data: dict, *args, **filter_by) -> Optional[T]: ...

    @abstractmethod
    async def delete_one(self, *args, **filter_by) -> None: ...



class SQLAlchemyORMRepository(AbstractRepository[T]):
    cls_model: Optional[Type[T]] = None

    def __init__(self, model: Optional[Type[T]] = None):
        orm_model: Optional[Type[T]] = model or self.__class__.cls_model
        if not orm_model:
            raise ValueError("You must pass the model in a class or in a method __init__.")
        self.model: Type[T] = orm_model

    @with_session
    async def add_one(self, session: AsyncSession, data: dict[str, Any]) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
        except Exception as err:
            raise err

    @with_session
    async def find_one(self, session: AsyncSession, **filter_by) -> Optional[T]:
        stmt = select(self.model).filter_by(**filter_by).limit(1)
        try:
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as err:
            raise err

    @with_session
    async def find_all(
        self, session: AsyncSession, order_by: Optional[list[tuple[str, str]]] = None, **filter_by
    ) -> Sequence[T]:
        stmt = select(self.model).filter_by(**filter_by)

        if not order_by:
            order_by = []

        order_by_clauses = []
        try:
            for field_name, direction in order_by:
                if not hasattr(self.model, field_name):
                    raise ValueError(
                        f"Field '{field_name}' does not exist on model '{self.model.__name__}'"
                    )
                column = getattr(self.model, field_name)
                if direction.lower() == "asc":
                    order_by_clauses.append(asc(column))
                elif direction.lower() == "desc":
                    order_by_clauses.append(desc(column))
                else:
                    raise ValueError(
                        f"Invalid sort direction '{direction}' for field '{field_name}'. Use 'asc' or 'desc'."
                    )

            stmt = stmt.order_by(*order_by_clauses)

            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as err:
            raise err

    @with_session
    async def update_one(self, session: AsyncSession, data: dict, **filter_by) -> Optional[T]:
        stmt = update(self.model).filter_by(**filter_by).values(**data).returning(self.model)
        try:
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            await session.commit()
            return obj
        except Exception as err:
            raise err

    @with_session
    async def delete_one(self, session: AsyncSession, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        try:
            await session.execute(stmt)
            await session.commit()
        except Exception as err:
            raise err
