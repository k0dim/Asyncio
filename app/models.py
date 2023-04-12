import asyncio

from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from cachetools import cached

from config import DNS

Base = declarative_base()


class StarWars(Base):
    __tablename__ = "starwars"

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(20))
    eye_color = Column(String(20))
    films = Column(String)
    gender = Column(String(20))
    hair_color = Column(String(20))
    height = Column(String(10))
    homeworld = Column(String)
    mass = Column(String(10))
    name = Column(String(50))
    skin_color = Column(String(20))
    species = Column(String)
    starships = Column(String)
    url = Column(String(50))
    vehicles = Column(String)


@cached({})
def get_engine():
    return create_async_engine(DNS)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine(), class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with create_async_engine(DNS).begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await create_async_engine(DNS).dispose()

ORM_MODEL = StarWars


if __name__ == "__main__":
    asyncio.run(init_models())