from typing import List

from sqlalchemy.orm import Session

from app.models.models import ConferenceRoomModel, UserModel
from app.schemas.entities import ConferenceRoomCreateRequest, UserSchema


class ConferenceRoomRepository:
    def __init__(self, db: Session, user: UserSchema):
        self.db = db
        self.user = user

    async def get(self) -> List[ConferenceRoomModel]:
        return (
            self.db.query(ConferenceRoomModel)
            .join(ConferenceRoomModel.manager)
            .filter(UserModel.company_id == self.user.company_id)
            .all()
        )

    async def create(
        self, data: ConferenceRoomCreateRequest
    ) -> ConferenceRoomModel:
        new_room = ConferenceRoomModel(**data.model_dump())
        self.db.add(new_room)
        self.db.commit()
        self.db.refresh(new_room)

        return new_room
