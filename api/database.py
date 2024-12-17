from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy
import os
from collections.abc import AsyncGenerator

class Base(DeclarativeBase):
    pass


class Account(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "account"
    role = sqlalchemy.Column(sqlalchemy.String(16), nullable=False)
    account_name = sqlalchemy.Column(sqlalchemy.String(32), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(80), nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(1024), nullable=False)


DATABASE_URL = os.environ.get(
    "DATABASE_URL", "mysql+asyncmy://root:admin@localhost:3306/AUTH_DEMO"
)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
