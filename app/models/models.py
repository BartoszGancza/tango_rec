import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base


class ConferenceRoomModel(Base):
    __tablename__ = "conference_rooms"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manager = relationship("UserModel", back_populates="conference_rooms")
    manager_id = Column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), index=True
    )
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    calendar_events = relationship(
        "CalendarEventModel", back_populates="location"
    )


class UserModel(Base):
    __tablename__ = "users"

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    company_id = Column(UUID(as_uuid=True), index=True)
    conference_rooms = relationship(
        "ConferenceRoomModel", back_populates="manager"
    )
    calendar_events = relationship(
        "CalendarEventModel",
        secondary="calendar_event_attendees",
        back_populates="attendees",
    )
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    timezone = Column(String, nullable=False)


class CalendarEventModel(Base):
    __tablename__ = "calendar_events"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = relationship("UserModel", back_populates="calendar_events")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), index=True)
    company_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    location = relationship(
        "ConferenceRoomModel",
        back_populates="calendar_events",
    )
    location_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conference_rooms.uuid"),
        nullable=True,
        index=True,
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    agenda = Column(String, nullable=False)
    attendees = relationship(
        "UserModel",
        secondary="calendar_event_attendees",
        back_populates="calendar_events",
    )


class CalendarEventAttendees(Base):
    __tablename__ = "calendar_event_attendees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), index=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("calendar_events.uuid"))
