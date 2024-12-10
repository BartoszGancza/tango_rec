import json

from app.models.models import ConferenceRoomModel, UserModel
from app.schemas.entities import ConferenceRoomSchema

USER = {
    "uuid": "699b2e59-92b5-4c2f-868f-c89128b96156",
    "username": "testuser",
    "email": "tony@stark.com",
    "timezone": "Europe/Warsaw",
    "company_id": "699b2e59-92b5-4c2f-868f-c89128b96156",
    "password": "password",
}

conference_room_obj1 = {
    "uuid": "699b2e59-92b5-4c2f-868f-c89128b96156",
    "name": "testroom",
    "address": "testaddress",
    "manager_id": "699b2e59-92b5-4c2f-868f-c89128b96156",
}
conference_room_obj2 = {
    "uuid": "699b2e59-92b5-4c2f-868f-c89128b96156",
    "name": "anothertestroom",
    "address": "someaddress",
    "manager_id": "699b2e59-92b5-4c2f-868f-c89128b96156",
}

CONFERENCE_ROOMS = [
    ConferenceRoomModel(**conference_room_obj1),
    ConferenceRoomModel(**conference_room_obj2),
]

for room in CONFERENCE_ROOMS:
    room.manager = UserModel(**USER)
    room.calendar_events = []

CONFERENCE_ROOMS_SCHEMA = [
    json.loads(ConferenceRoomSchema.model_validate(room).model_dump_json())
    for room in CONFERENCE_ROOMS
]

CONFERENCE_ROOM_POST = {
    "name": "testroom",
    "address": "testaddress",
    "manager_id": "699b2e59-92b5-4c2f-868f-c89128b96156",
}
