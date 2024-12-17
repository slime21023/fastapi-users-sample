from fastapi import Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from api.database import Account, get_async_session
from api.auth.manager import AccountManager
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
import uuid


SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600, algorithm="HS256")


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)


async def get_account_database(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, Account)


async def get_account_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_account_database),
):
    yield AccountManager(user_db)


# Create the FastAPIUsers Router
fastapi_users = FastAPIUsers[Account, uuid.UUID](get_account_manager, [auth_backend])


# The dependency to get the current user
current_user = fastapi_users.current_user(active=True)
