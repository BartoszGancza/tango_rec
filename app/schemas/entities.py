import datetime
from typing import List, Optional
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field


class UserEmailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str


class UserSchema(UserEmailSchema):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    company_id: UUID
    username: str
    timezone: str
    password: str = Field(..., exclude=True)


class LocationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    address: str


class CalendarEventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    owner: UserEmailSchema
    start_time: datetime.datetime
    end_time: datetime.datetime
    name: str
    agenda: str
    attendees: List[UserEmailSchema]
    location: Optional[LocationSchema] = None

    def convert_to_user_timezone(self, user_timezone: str):
        user_timezone = ZoneInfo(user_timezone)
        utc_timezone = ZoneInfo("UTC")
        self.start_time = self.start_time.replace(
            tzinfo=utc_timezone
        ).astimezone(user_timezone)
        self.end_time = self.end_time.replace(tzinfo=utc_timezone).astimezone(
            user_timezone
        )
        return self


class ConferenceRoomSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    manager: UserEmailSchema
    name: str
    address: str


class EventRetrieveRequest(BaseModel):
    date: Optional[datetime.date] = None
    location_id: Optional[UUID] = None
    query: Optional[str] = None

    def convert_date_to_utc(self, user_timezone: str):
        if self.date:
            self.date = (
                datetime.datetime.combine(
                    self.date, datetime.datetime.min.time()
                )
                .replace(tzinfo=ZoneInfo(user_timezone))
                .astimezone(ZoneInfo("UTC"))
            )
        return self


class EventCreateRequest(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime
    participants: List[str]
    agenda: str
    location_id: Optional[UUID] = None
    name: str

    def convert_to_utc(self, user_timezone: str):
        user_timezone = ZoneInfo(user_timezone)
        utc_timezone = ZoneInfo("UTC")
        self.start_time = self.start_time.replace(
            tzinfo=user_timezone
        ).astimezone(utc_timezone)
        self.end_time = self.end_time.replace(tzinfo=user_timezone).astimezone(
            utc_timezone
        )
        return self


class ConferenceRoomCreateRequest(BaseModel):
    name: str
    address: str
    manager_id: UUID
