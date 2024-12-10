from sqlalchemy.orm import Session

from app.repositories.rooms import ConferenceRoomRepository
from app.schemas.entities import ConferenceRoomCreateRequest, UserSchema


class ConferenceRoomService:
    def __init__(self, db: Session, user: UserSchema):
        self.db = db
        self.user = user

    async def get_rooms(self):
        return await ConferenceRoomRepository(db=self.db, user=self.user).get()

    async def create_room(self, data: ConferenceRoomCreateRequest):
        return await ConferenceRoomRepository(db=self.db, user=self.user).create(
            data=data
        )
