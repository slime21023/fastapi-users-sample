import uuid
from typing import Optional
from fastapi_users import schemas



class UserRead(schemas.BaseUser[uuid.UUID]):
    account_name: str
    role: str


class UserCreate(schemas.BaseUserCreate):
    account_name: str
    role: str


class UserUpdate(schemas.BaseUserUpdate):
    account_name: Optional[str]
    role: Optional[str]
