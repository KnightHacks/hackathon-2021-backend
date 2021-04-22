# flake8: noqa
import json
from src.models.event import Event
from tests.base import BaseTestCase
import datetime

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

    """update_event (worked on by Conroy)"""

    def test_update_event(self):
        
        Event.createOne(
            name = "Python Workshop",
            date_time = "2020-09-11T11:30:00",
            image = "https://www.fancyimg.com/myimg",
            link = "https://ucf.zoom.us/blahblahblah",
            end_date_time = "2020-09-11T12:30:00",
            attendees_count = 999,
            event_status = "open"
        )
        
        res = self.client.put(
            "/api/events/update_event/Python Workshop/",
            data=json.dumps({"attendees_count": 20}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201)

        updated_event = Event.findOne(name="Python Workshop")
        
        self.assertEqual(updated_event.attendees_count, 20)

    def test_update_event_date_time(self):
        
        Event.createOne(
            name = "Python Workshop",
            date_time = "2020-09-11T11:30:00",
            image = "https://www.fancyimg.com/myimg",
            link = "https://ucf.zoom.us/blahblahblah",
            end_date_time = "2020-09-11T12:30:00",
            attendees_count = 999,
            event_status = "open"
        )
        
        res = self.client.put(
            "/api/events/update_event/Python Workshop/",
            data=json.dumps({
                "date_time": "2021-09-11T11:30:00",
                "end_date_time": "2021-09-11T12:30:00"}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 201)

        updated_event = Event.findOne(name="Python Workshop")
        
        self.assertEqual(updated_event.date_time, datetime.datetime(2021, 9, 11, 11, 30))
        self.assertEqual(updated_event.end_date_time, datetime.datetime(2021, 9, 11, 12, 30))

    def test_update_event_invalid_json(self):
        
        Event.createOne(
            name = "Python Workshop",
            date_time = "2020-09-11T11:30:00",
            image = "https://www.fancyimg.com/myimg",
            link = "https://ucf.zoom.us/blahblahblah",
            end_date_time = "2020-09-11T12:30:00",
            attendees_count = 999,
            event_status = "open"
        )
        
        res = self.client.put(
            "/api/events/update_event/Python Workshop/",
            data=json.dumps({}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)

    def test_update_event_not_found(self):

        res = self.client.put(
            "/api/events/update_event/Python Workshop/",
            data=json.dumps({"attendees_count": 20}),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 404)
