from typing import List

from fastapi import APIRouter, Depends, Query

from app.routers.auth import get_user
from app.schemas.entities import (
    CalendarEventSchema,
    EventCreateRequest,
    EventRetrieveRequest,
)
from app.services.events import EventService
from config.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CalendarEventSchema])
async def get_events_with_filters(
    data: EventRetrieveRequest = Query(),
    db: get_db = Depends(),
    user: get_user = Depends(),
):
    return await EventService(db=db, user=user).get_events(data=data)


@router.post("/", response_model=CalendarEventSchema)
async def create_event(
    data: EventCreateRequest, db: get_db = Depends(), user: get_user = Depends()
):
    return await EventService(db=db, user=user).create_event(data=data)
