from os import getenv
from dotenv import load_dotenv
from typing import AsyncGenerator, Generator

from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

load_dotenv()

DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
 

URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(URL, echo=True)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)



class Base(DeclarativeBase):
    ...


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        
        
# async def get_db() -> Generator:
#     try:
#         session: AsyncSession = async_session()
#         yield session
#     finally:
#         await session.close()




