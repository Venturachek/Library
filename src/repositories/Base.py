import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, update, delete, select
from sqlalchemy.exc import IntegrityError

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.Mapper.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__ (self, session):
        self.session = session


    async def get_all(self):
        try:
            query = select(self.model)
            res = await self.session.execute(query)
        except ObjectNotFoundException:
            raise ObjectNotFoundException
        return [self.mapper.map_to_domain(model) for model in res.scalars().all()]

    async def get_filter_by(self, **filter_by):
        try:
            query = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(query)
        except ObjectNotFoundException:
            raise ObjectNotFoundException
        result = res.scalars().one()
        return self.mapper.map_to_domain(result)


    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            res = await self.session.execute(add_stmt)
        except IntegrityError as ex:
            logging.error(f"{data} addition was interrupted {type(ex.orig.__cause__)=}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.error(f"Unknown error: Failed to add {data} due to {type(ex.orig.__cause__)}")
                raise ex
        model = res.scalars().one()
        return self.mapper.map_to_domain(model)


    async def add_bulk(self, data: list[BaseModel]):
        try:
            add_stmt = insert(self.model).values([model.model_dump() for model in data])
            await self.session.execute(add_stmt)
        except IntegrityError as ex:
            print(type(ex.orig.__cause__))
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                raise ex


    async def edit(self, data: BaseModel, **filter_by):
        edit_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(edit_stmt)
        result = res.scalars().one()
        return self.mapper.map_to_domain(result)


    async def delete(self, **filter_by):
        try:
            delete_stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_stmt)
        except ObjectNotFoundException:
            raise ObjectNotFoundException

    async def patch(self, data: BaseModel, **filter_by):
        patch_stmt = update(self.model).values(**data.model_dump(exclude_unset=True)).filter_by(**filter_by).returning(self.model)
        res = await self.session.execute(patch_stmt)
        result = res.scalars().one()
        return self.mapper.map_to_domain(result)