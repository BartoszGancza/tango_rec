from datetime import timedelta
from typing import List

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.models import CalendarEventModel, ConferenceRoomModel, UserModel
from app.schemas.entities import (
    EventCreateRequest,
    EventRetrieveRequest,
    UserSchema,
)


class EventRepository:
    def __init__(self, db: Session, user: UserSchema):
        self.db = db
        self.user = user

    async def get(self, data: EventRetrieveRequest) -> List[CalendarEventModel]:
        q = (
            self.db.query(CalendarEventModel)
            .options(
                joinedload(CalendarEventModel.attendees),
                joinedload(CalendarEventModel.location),
                joinedload(CalendarEventModel.owner),
            )
            .join(CalendarEventModel.owner)
            .join(CalendarEventModel.location, isouter=True)
            .filter(
                CalendarEventModel.company_id == self.user.company_id,
                or_(
                    UserModel.uuid == self.user.uuid,
                    ConferenceRoomModel.manager_id == self.user.uuid,
                    CalendarEventModel.attendees.any(
                        UserModel.uuid == self.user.uuid
                    ),
                ),
            )
        )

        if date := data.date:
            q = q.filter(
                CalendarEventModel.start_time >= date,
                CalendarEventModel.start_time <= date + timedelta(days=1),
            )
        if location := data.location_id:
            q = q.filter(CalendarEventModel.location_id == location)
        if query := data.query:
            query_strings = query.split("+")
            search_args = [
                col.ilike(f"%{word}%")
                for col in [CalendarEventModel.name, CalendarEventModel.agenda]
                for word in query_strings
            ]
            q = q.filter(
                or_(*search_args),
            )

        return q.all()

    async def create(self, data: EventCreateRequest):
        data = data.dict()
        location_id = data.get("location_id")

        if location_id and (
            not self.db.query(ConferenceRoomModel)
            .join(ConferenceRoomModel.manager)
            .filter(
                ConferenceRoomModel.uuid == location_id,
                UserModel.company_id == self.user.company_id,
            )
            .first()
        ):
            raise HTTPException(
                status_code=400,
                detail="Given location not found.",
            )

        participants = data.pop("participants")
        new_event = CalendarEventModel(**data)
        self.db.add(new_event)
        new_event.owner_id = self.user.uuid
        new_event.company_id = self.user.company_id

        participant_users = (
            self.db.query(UserModel)
            .filter(UserModel.email.in_(participants))
            .all()
        )

        new_event.attendees = participant_users
        self.db.commit()
        self.db.refresh(new_event)

        return new_event
