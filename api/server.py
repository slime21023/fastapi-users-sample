from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.database import create_db_and_tables
from api.auth.backend import fastapi_users, auth_backend
from api.auth.schema import UserRead, UserCreate, UserUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# The Router with `/login` and `logout` endpoints
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


# The Router with `register` route to allow a user to create a new account
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# The verify route for managing user email verification
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# The reset password route with `/forgot-password` and `/reset-password` endpoints
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


# The user router to manage user accounts
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)