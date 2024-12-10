from sqlalchemy.orm import Session

from app.models.models import UserModel


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get(self, username: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.username == username).first()
