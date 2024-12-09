from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

# DATABASE_URL = f"sqlite+aiosqlite:///test.db"
#
# Base: DeclarativeMeta = declarative_base()
#
# engine = create_async_engine(DATABASE_URL)

# from config import DB_CONNECTION

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine('postgresql+asyncpg://sasha:NOV87CMvgEy7OKXP7kkOn0tgAUENFAeL@dpg-ctad51jtq21c73c3jvpg-a.oregon-postgres.render.com/lab3_au3f')



async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session