from typing import List

from fastapi import APIRouter, Depends

from app.routers.auth import get_user
from app.schemas.entities import (
    ConferenceRoomCreateRequest,
    ConferenceRoomSchema,
)
from app.services.rooms import ConferenceRoomService
from config.database import get_db

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ConferenceRoomSchema])
async def get_conference_rooms(
    db: get_db = Depends(), user: get_user = Depends()
):
    return await ConferenceRoomService(db=db, user=user).get_rooms()


@router.post("/", response_model=ConferenceRoomSchema)
async def create_conference_room(
    data: ConferenceRoomCreateRequest,
    db: get_db = Depends(),
    user: get_user = Depends(),
):
    return await ConferenceRoomService(db=db, user=user).create_room(data=data)
