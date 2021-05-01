# flake8: noqa
import json
from src.models.event import Event
from tests.base import BaseTestCase


class TestEventsBlueprint(BaseTestCase):
    """Tests for the Events Endpoints"""

    """create_event"""

    def test_create_event(self):
        pass

    def test_create_event_invalid_json(self):
        res = self.client.post("/api/events/create_event/", data=json.dumps({}))

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")

    def test_create_event_invalid_datatypes(self):
        pass

    """update_event"""

    def test_update_event(self):
        pass

    def test_update_event_invalid_json(self):
        pass

    def test_update_event_not_found(self):
        pass
