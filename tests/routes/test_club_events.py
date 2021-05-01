# flake8: noqa
import json
from src.models.club_event import ClubEvent
from tests.base import BaseTestCase
from datetime import datetime, timedelta
from src.models.user import ROLES


class TestClubEventsBlueprint(BaseTestCase):
    """Tests for the Club Events Endpoints"""

    """update_events"""

    def test_update_events(self):
        # Gets a token of an admin user to do the request
        token = self.login_user(ROLES.ADMIN)

        # Creates a mock request to the update_event endpoint
        res = self.client.put(
            "/api/club/update_events/",
            data=json.dumps(
                [
                    {
                        "date": "2014-09-10T11:41:00",
                        "description": "An introductory workshop for the Python language.",
                        "location": "https://www.zoom.com",
                        "name": "string",
                        "presenter": "string",
                        "tags": ["string"],
                    }
                ]
            ),
            headers=[("sid", token)],
            content_type="application/json",
        )

        # ensure that the club event was successfully created
        self.assertEqual(res.status_code, 201)

        # Ensures at least a single event is available
        self.assertEqual(ClubEvent.objects.count(), 1)

    def test_update_events_bad_event(self):
        token = self.login_user(ROLES.ADMIN)
        res = self.client.put(
            "/api/club/update_events/",
            headers=[("sid", token)],
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_update_events_invalid_json(self):
        token = self.login_user(ROLES.ADMIN)
        res = self.client.put(
            "/api/club/update_events/",
            data=json.dumps([{}]),
            content_type="application/json",
            headers=[("sid", token)],
        )

        # ensure that the club event was unsuccessfully created (due to invalid json file)
        self.assertEqual(res.status_code, 400)

        # ensure that no clubevent  objects exist in MonogDB
        self.assertEqual(ClubEvent.objects.count(), 0)

    def test_update_events_invalid_datatypes(self):
        # Gets a token of an admin user to do the request
        token = self.login_user(ROLES.ADMIN)

        res = self.client.put(
            "/api/club/update_events/",
            data=json.dumps(
                [
                    {
                        "date": "2014-09-10T11:41:00",
                        "description": "An introductory workshop for the Python language.",
                        "location": 123,
                        "name": "string",
                        "presenter": "string",
                        "tags": ["string"],
                    },
                    {
                        "date": "2014-09-10T11:41:00",
                        "description": "Rust lecture",
                        "location": 123,
                        "name": "string",
                        "presenter": "string",
                        "tags": ["string"],
                    },
                ]
            ),
            headers=[("sid", token)],
            content_type="application/json",
        )

        # Ensure that the sponsor was unsuccessfully created due to not being unique
        self.assertEqual(res.status_code, 400)

        # Ensure that only 1 sponsor object exists in MonogDB
        self.assertEqual(ClubEvent.objects.count(), 0)

    """get_events"""

    def test_get_events(self):
        new_club_event = ClubEvent.createOne(
            date="2014-09-10T11:41:00.12343-03:00",
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
            date="2014-09-10T11:41:00.12343-03:00",
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
            date=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            date=datetime.now() - timedelta(days=1),
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
            date=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            date=datetime.now() + timedelta(days=7),
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
            date=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            date=datetime.now() + timedelta(days=30),
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
            date=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            date=datetime.now() + timedelta(days=365),
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
            date=datetime.now(),
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
            date=datetime.now(),
            description="An introductory workshop for the Python language.",
            location="https://www.zoom.com",
            name="string",
            presenter="string",
            tags=["string"],
        )

        ClubEvent.createOne(
            date=datetime.now(),
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
