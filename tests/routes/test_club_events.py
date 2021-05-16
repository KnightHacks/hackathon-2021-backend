# flake8: noqa
import json
from src.models.club_event import ClubEvent
from tests.base import BaseTestCase
from datetime import datetime, timedelta
from src.models.user import ROLES


class TestClubEventsBlueprint(BaseTestCase):
    """Tests for the Club Events Endpoints"""

    """get_events"""

    def test_get_events(self):
        new_club_event = ClubEvent.createOne(
            start="2014-09-10T11:41:00.12343-03:00",
            end="2014-09-10T11:41:00.12343-03:00",
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        # Mocks a get request to the club events route
        res = self.client.get("/api/club/get_events/")

        # Checks that we returns a successful status
        self.assertEqual(res.status_code, 200)

    def test_get_events_mix_rdate_startend_dates(self):
        res = self.client.get("/api/club/get_events/?rdate=Today&start_date=testdate")

        self.assertEqual(res.status_code, 400)

    def test_get_events_confirmed_with_dates(self):
        # One that has a date
        ClubEvent.createOne(
            start="2014-09-10T11:41:00.12343-03:00",
            end="2014-09-10T11:41:00.12343-03:00",
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        # One that does not have a date
        ClubEvent.createOne(
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        res = self.client.get("/api/club/get_events/")

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_rdate_today(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            start=datetime.now() - timedelta(days=1),
            end=datetime.now() - timedelta(days=1),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        res = self.client.get("/api/club/get_events/?rdate=Today")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_rdate_nextweek(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            start=datetime.now() + timedelta(days=7),
            end=datetime.now() + timedelta(days=7),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        res = self.client.get("/api/club/get_events/?rdate=NextWeek")

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_rdate_nextmonth(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            start=datetime.now() + timedelta(days=30),
            end=datetime.now() + timedelta(days=30),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        res = self.client.get("/api/club/get_events/?rdate=NextMonth")

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_rdate_nextyear(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            start=datetime.now() + timedelta(days=365),
            end=datetime.now() + timedelta(days=365),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        res = self.client.get("/api/club/get_events/?rdate=NextYear")

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_not_confirmed(self):
        res = self.client.get("api/club/get_events/?rdate=NextWeek&confirmed=false")
        self.assertEqual(res.status_code, 400)

    def test_get_events_start_end_date(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        res = self.client.get(
            f"/api/club/get_events/?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(data["count"], 1)

    def test_get_events_if_count(self):
        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            start=datetime.now(),
            end=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )
        res = self.client.get("/api/club/get_events/?count=1")

        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data.decode())
        self.assertEqual(len(data["events"]), 1)
