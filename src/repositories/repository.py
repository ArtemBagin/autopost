from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        res = self.model(**data)
        self.session.add(res)
        await self.session.commit()
        return res

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.scalar_one()

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = res.all()
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.first()
        return res

    async def find(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalars().all()
        return res

    async def delete_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        await self.session.delete(res)
        await self.session.commit()

