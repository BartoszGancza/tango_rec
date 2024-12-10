import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.events import EventRepository
from app.schemas.entities import (
    CalendarEventSchema,
    EventCreateRequest,
    EventRetrieveRequest,
    UserSchema,
)


class EventService:
    def __init__(self, db: Session, user: UserSchema):
        self.db = db
        self.user = user

    async def get_events(self, data: EventRetrieveRequest):
        events = await EventRepository(db=self.db, user=self.user).get(
            data=data.convert_date_to_utc(user_timezone=self.user.timezone)
        )

        return list(
            map(
                lambda event: CalendarEventSchema.model_validate(
                    event
                ).convert_to_user_timezone(user_timezone=self.user.timezone),
                events,
            )
        )

    async def create_event(self, data: EventCreateRequest):
        if data.end_time - data.start_time > datetime.timedelta(hours=8):
            raise HTTPException(
                status_code=400,
                detail="Event duration should not exceed 8 hours",
            )

        created_event = await EventRepository(
            db=self.db, user=self.user
        ).create(data=data.convert_to_utc(user_timezone=self.user.timezone))
        event_schema = CalendarEventSchema.model_validate(created_event)

        return event_schema.convert_to_user_timezone(
            user_timezone=self.user.timezone
        )
