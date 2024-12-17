import os
from typing import Optional
from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from api.database import Account
import uuid

AUTH_SECRET = os.environ.get(
    "AUTH_SECRET", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)


# Custom user manager
class AccountManager(UUIDIDMixin, BaseUserManager[Account, uuid.UUID]):
    reset_password_token_secret = AUTH_SECRET
    verification_token_secret = AUTH_SECRET

    async def on_after_register(
        self, account: Account, request: Optional[Request] = None
    ):
        print(f"Account {account.id} has registered.")

    async def on_after_forgot_password(
        self, account: Account, token: str, request: Optional[Request] = None
    ):
        print(f"Account {account.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, account: Account, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for account {account.id}. Verification token: {token}"
        )
