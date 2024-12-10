from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app as application
from app.schemas.entities import UserSchema
from tests.consts import USER

client = TestClient(application)


async def override_get_user():
    return UserSchema.model_validate(USER)


async def override_user_auth_auth_fail():
    raise HTTPException(status_code=401, detail="Unauthorized")


async def mock_get_db():
    return Session()
