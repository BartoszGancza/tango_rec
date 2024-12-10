import json

from app.main import app as application
from app.routers.auth import get_user
from config.database import get_db
from tests.consts import CONFERENCE_ROOM_POST, CONFERENCE_ROOMS_SCHEMA
from tests.setup_tests import (
    client,
    mock_get_db,
    override_get_user,
    override_user_auth_auth_fail,
)


class TestRooms:
    def setup_method(self, method):
        application.dependency_overrides[get_user] = override_get_user
        application.dependency_overrides[get_db] = mock_get_db

    def teardown_method(self, method):
        application.dependency_overrides = {}

    def test_get_conference_rooms(self, mock_rooms_return):
        response = client.get("/rooms")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert json.loads(response.text) == CONFERENCE_ROOMS_SCHEMA

    def test_create_conference_rooms(self, mock_create_room_return):
        response = client.post("/rooms", json=CONFERENCE_ROOM_POST)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert json.loads(response.text) == CONFERENCE_ROOMS_SCHEMA[0]


class TestRoomsUserAuthFail:
    def setup_method(self, method):
        application.dependency_overrides[
            get_user
        ] = override_user_auth_auth_fail
        application.dependency_overrides[get_db] = mock_get_db

    def teardown_method(self, method):
        application.dependency_overrides = {}

    def test_get_conference_rooms(self, mock_rooms_return):
        response = client.get("/rooms")
        assert response.status_code == 401
        assert response.headers["content-type"] == "application/json"
        assert json.loads(response.text) == {"detail": "Unauthorized"}

    def test_create_conference_rooms(self, mock_create_room_return):
        response = client.post("/rooms", json=CONFERENCE_ROOM_POST)
        assert response.status_code == 401
        assert response.headers["content-type"] == "application/json"
        assert json.loads(response.text) == {"detail": "Unauthorized"}
