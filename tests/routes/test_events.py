# flake8: noqa
import json
from src.models.event import Event
from src.models.sponsor import Sponsor
from src.models.user import User, ROLES
from tests.base import BaseTestCase
from datetime import datetime


class TestEventsBlueprint(BaseTestCase):
    """Tests for the Events Endpoints"""

    """create_event"""

    def test_create_event(self):
        now = datetime.now()

        Sponsor.createOne(sponsor_name="new_sponsor",
                          logo="https://blob.knighthacks.org/somelogo.png",
                          subscription_tier="Gold",
                          email="sponsor@email.com",
                          username="new_sponsor",
                          password="password",
                          roles=ROLES.SPONSOR)
        
        User.createOne(username="new_user",
                       email="new@email.com",
                       password="new_password",
                       roles=ROLES.HACKER)
        
        res = self.client.post(
            "/api/events/create_event/",
            data=json.dumps({
                "name": "new_event",
                "date_time": now.isoformat(),
                "description": "description",
                "image": "https://blob.knighthacks.org/somelogo.png",
                "link": "https://blob.knighthacks.org/somelogo.png",
                "end_date_time": now.isoformat(),
                "attendees_count": 10,
                "event_status": "status",
                "sponsors": ["new_sponsor"],
                "user": "new_user"
            }),
            content_type="application/json")
        
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Event.objects.count(), 1)

    def test_create_event_invalid_json(self):
        res = self.client.post("/api/events/create_event/", data=json.dumps({}))

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")

    def test_create_event_invalid_datatypes(self):
        Sponsor.createOne(username="new_sponsor",
                          email="new@email.com",
                          password="new_password",
                          roles=ROLES.SPONSOR,
                          sponsor_name="new_sponsor")

        res = self.client.post(
            "api/events/create_event/",
            data=json.dumps({
                "name": 12345,
                "date_time": "newdate",
                "description": 12345,
                "image": 12345,
                "link": 12345,
                "end_date_time": "anotherdate",
                "attendees_count": "newcount",
                "event_status": 12345,
                "sponsors": "new_sponsor",
                "users": "new_user"
            }),
            content_type="application/json")
        
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")

    """update_event"""

    def test_update_event(self):
        now = datetime.now()
        
        Event.createOne(name="new_event",
                        date_time=now.isoformat(),
                        description="description",
                        image="https://blob.knighthacks.org/somelogo.png",
                        link="https://blob.knighthacks.org/somelogo.png",
                        end_date_time=now.isoformat(),
                        attendees_count=10,
                        event_status="status")

        res = self.client.put(
            "api/events/update_event/new_event/",
            data=json.dumps({
                "date_time": now.isoformat(),
                "description": "another_description",
                "image": "https://blob.knighthacks.org/somelogo.png",
                "link": "https://blob.knighthacks.org/somelogo.png",
                "end_date_time": now.isoformat(),
                "attendees_count": 20,
                "event_status": "ongoing",
            }),
            content_type="application/json")

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Event.objects.first().event_status, "ongoing")

    def test_update_event_invalid_json(self):
        now = datetime.now()

        Event.createOne(name="new_event",
                        date_time=now.isoformat(),
                        description="description",
                        image="https://blob.knighthacks.org/somelogo.png",
                        link="https://blob.knighthacks.org/somelogo.png",
                        end_date_time=now.isoformat(),
                        attendees_count=10,
                        event_status="status",
                        user="new_user")
        
        res = self.client.put("api/events/update_event/new_event/", data=json.dumps({}))
        
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")

    def test_update_event_not_found(self):
        res = self.client.put(
            "api/events/update_event/new_event/",
            data=json.dumps({
                "description": "new description"
            }),
            content_type="application/json")
        
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["name"], "Not Found")

    """get_all_events"""

    def test_get_all_events(self):
        now = datetime.now()
        
        User.createOne(username="new_user",
                       email="another_new@email.com",
                       password="new_password",
                       roles=ROLES.HACKER)
        
        Event.createOne(name="new_event",
                        date_time=now.isoformat(),
                        description="description",
                        image="https://blob.knighthacks.org/somelogo.png",
                        link="https://blob.knighthacks.org/somelogo.png",
                        end_date_time=now.isoformat(),
                        attendees_count=10,
                        event_status="status",
                        user="new_user")
        
        Event.createOne(name="another_new_event",
                        date_time=now.isoformat(),
                        description="description",
                        image="https://blob.knighthacks.org/somelogo.png",
                        link="https://blob.knighthacks.org/somelogo.png",
                        end_date_time=now.isoformat(),
                        attendees_count=10,
                        event_status="status",
                        user="new_user")
        
        res = self.client.get("api/events/get_all_events/")

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["events"][0]["name"], "new_event")
        self.assertEqual(data["events"][1]["name"], "another_new_event")

    def test_get_all_events_not_found(self):
        res = self.client.get("api/events/get_all_events/")
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["name"], "Not Found")