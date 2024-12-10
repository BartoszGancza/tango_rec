import hashlib

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.repositories.auth import AuthRepository
from app.schemas.entities import UserSchema


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    async def hash_password(password: str) -> str:
        password_bytes = password.encode("utf-8")
        sha = hashlib.sha256()
        sha.update(password_bytes)

        return sha.hexdigest()

    async def get_user(
        self, form_data: OAuth2PasswordRequestForm
    ) -> UserSchema:
        user = await AuthRepository(db=self.db).get(username=form_data.username)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        user = UserSchema.model_validate(user)

        hashed_password = await self.hash_password(form_data.password)
        if not hashed_password == user.password:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        return user

    async def get_user_by_token(self, username: str) -> UserSchema:
        user = await AuthRepository(db=self.db).get(username=username)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid token")

        return UserSchema.model_validate(user)
