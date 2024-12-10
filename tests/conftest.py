import pytest

from app.repositories.rooms import ConferenceRoomRepository
from tests.consts import CONFERENCE_ROOMS


@pytest.fixture(autouse=True)
def no_connections(mocker):
    """Stop all httpx and DB connections from happening during tests."""
    mocker.patch("httpx._client.AsyncClient.request", return_value=None)
    mocker.patch("sqlalchemy.orm.session.Session.query", return_value=None)
    mocker.patch("sqlalchemy.orm.session.Session.commit", return_value=None)
    mocker.patch("sqlalchemy.orm.session.Session.add", return_value=None)
    mocker.patch("sqlalchemy.orm.session.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.session.Session.refresh", return_value=None)


@pytest.fixture
def mock_rooms_return(mocker):
    mocker.patch.object(
        ConferenceRoomRepository,
        "get",
        return_value=CONFERENCE_ROOMS,
        autospec=True,
    )


@pytest.fixture
def mock_create_room_return(mocker):
    mocker.patch.object(
        ConferenceRoomRepository,
        "create",
        return_value=CONFERENCE_ROOMS[0],
        autospec=True,
    )
