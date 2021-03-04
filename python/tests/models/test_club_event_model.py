# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.club_event import ClubEvent
from tests.base import BaseTestCase
from datetime import datetime


class TestClubEventModel(BaseTestCase):
    """Tests for the ClubEvent Model"""

    def test_create_club_event(self):
        now = datetime.now()
        club_event = ClubEvent.createOne(name="foobar",
                                         tags=["tag1", "tag2"],
                                         presenter="Arjun",
                                         date=now,
                                         description="Lorem ipsum",
                                         location="link or actual loc")

        self.assertTrue(club_event.id)
        self.assertFalse(True)
        self.assertEqual(club_event.name, "foobar")
        self.assertEqual(club_event.tags, ["tag1", "tag2"])
        self.assertEqual(club_event.presenter, "Arjun")
        self.assertEqual(club_event.date, now)
        self.assertEqual(club_event.description, "Lorem ipsum")
        self.assertEqual(club_event.location, "link or actual loc")
