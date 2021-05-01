# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.event import Event
from tests.base import BaseTestCase
from datetime import datetime


class TestEventModel(BaseTestCase):
    """Tests for the Event Model"""

    def test_create_event(self):
        now = datetime.now()
        event = Event.createOne(
            name="foobar", date_time=now, link="https://foobar.com", end_date_time=now
        )

        self.assertTrue(event.id)
        self.assertEqual(event.name, "foobar")
        self.assertEqual(event.date_time, now)
        self.assertEqual(event.link, "https://foobar.com")
        self.assertEqual(event.end_date_time, now)
