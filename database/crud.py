from typing import Optional, Type

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database.base import Base
from database.setup import AsyncSessionLocal
from database.setup import engine

from utils.logger import logger


async def create_table(model: Type[Base]):
    async with engine.begin() as db:
        await db.run_sync(Base.metadata.create_all, tables=[model.__table__], checkfirst=True)
        logger.info("Table - Created or exists - %s", str(model.__table__))


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    except OSError as e:
        logger.error("Database - %s", str(e))
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database - %s", str(e))
        raise
    finally:
        await db.close()


async def get_table(db: AsyncSessionLocal, model: Type[Base], page: Optional[int] = None, per_page: Optional[int] = None):
    query = select(model)
    if page is not None and per_page is not None:
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
    result = await db.execute(query)
    return result.scalars().all()


async def get_row(db: AsyncSessionLocal, model: Type[Base], filter_):
    return await db.execute(select(model).where(filter_))
