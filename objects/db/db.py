import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from objects.schemas import *
from objects.schemas.base import Base

load_dotenv()

engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    echo=True,
)

sessionmaker = async_sessionmaker(engine)


async def init(engine) -> None:
    async with engine.connect() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS calculator"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
