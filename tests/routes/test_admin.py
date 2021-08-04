# flake8: noqa
import json
from src.models.hacker import Hacker
from src.models.sponsor import Sponsor
from src.models.user import ROLES
from tests.base import BaseTestCase
from datetime import datetime


class TestAdminBlueprint(BaseTestCase):
    """Tests for the Admin Endpoints"""

    """create_hacker"""

    def test_create_hacker(self):
        token = self.login_user(ROLES.ADMIN)
        now = datetime.now()
        res = self.client.post(
            "/api/admin/hackers/",
            data=json.dumps(
                {
                    "username": "foobar",
                    "email": "foobar@email.com",
                    "password": "123456"
                }
            ),
            content_type="application/json",
            headers=[("sid", token)]
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 1)

    def test_create_hacker_invalid_json(self):
        token = self.login_user(ROLES.ADMIN)
        res = self.client.post(
            "/api/admin/hackers/", data=json.dumps({}), content_type="application/json",
            headers=[("sid", token)]
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")
        self.assertEqual(Hacker.objects.count(), 0)

    def test_create_hacker_duplicate_user(self):
        token = self.login_user(ROLES.ADMIN)
        now = datetime.now()
        Hacker.createOne(
            username="foobar",
            email="foobar@email.com",
            password="123456",
            roles=ROLES.HACKER,
        )

        res = self.client.post(
            "/api/admin/hackers/",
            data=json.dumps(
                {
                    "username": "foobar",
                    "email": "foobar@email.com",
                    "password": "123456",
                    "date": now.isoformat(),
                }
            ),
            content_type="application/json",
            headers=[("sid", token)]
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 409)
        self.assertIn(
            "Sorry, that username or email already exists.", data["description"]
        )
        self.assertEqual(Hacker.objects.count(), 1)

    def test_create_hacker_invalid_datatypes(self):
        token = self.login_user(ROLES.ADMIN)
        res = self.client.post(
            "/api/admin/hackers/",
            data=json.dumps(
                {"username": "foobar", "email": "notanemail", "password": "123456"}
            ),
            content_type="application/json",
            headers=[("sid", token)]
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")
        self.assertEqual(Hacker.objects.count(), 0)

    def test_create_sponsor(self):
        token = self.login_user(ROLES.ADMIN)
        res = self.client.post(
            "/api/admin/sponsors/",
            data=json.dumps(
                {
                    "sponsor_name": "Bose",
                    "logo": "https://blob.knighthacks.org/somelogo.png",
                    "subscription_tier": "Gold",
                    "email": "bose@gmail.com",
                    "username": "boseofficial",
                    "password": "pass1234",
                }
            ),
            content_type="application/json", headers=[("sid", token)]
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_create_sponsor_invalid_json(self):
        token = self.login_user(ROLES.ADMIN)

        res = self.client.post(
            "/api/admin/sponsors/", data=json.dumps({}), content_type="application/json",
            headers=[("sid", token)]
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_create_sponsor_not_unique(self):
        token = self.login_user(ROLES.ADMIN)

        res = self.client.post(
            "/api/admin/sponsors/",
            data=json.dumps(
                {
                    "sponsor_name": "Bose",
                    "logo": "https://blob.knighthacks.org/somelogo.png",
                    "subscription_tier": "Gold",
                    "email": "bose@gmail.com",
                    "username": "boseofficial",
                    "password": "pass1234",
                }
            ),
            content_type="application/json", headers=[("sid", token)]
        )

        self.assertEqual(res.status_code, 201)

        res2 = self.client.post(
            "/api/admin/sponsors/",
            data=json.dumps(
                {
                    "sponsor_name": "Amazon",
                    "logo": "https://blob.knighthacks.org/somelogo.png",
                    "subscription_tier": "Gold",
                    "email": "amazon@gmail.com",
                    "username": "boseofficial",
                    "password": "pass1234",
                }
            ),
            content_type="application/json", headers=[("sid", token)]
        )

        self.assertEqual(res2.status_code, 409)
        self.assertEqual(Sponsor.objects.count(), 1)

    def test_create_sponsor_invalid_datatype(self):
        token = self.login_user(ROLES.ADMIN)

        res = self.client.post(
            "/api/sponsors/",
            data=json.dumps(
                {
                    "sponsor_name": "Google",
                    "logo": "https://blob.knighthacks.org/somelogo.png",
                    "subscription_tier": "Gold",
                    "email": 123,
                    "username": "googleofficial",
                    "password": "pass1234",
                }
            ),
            content_type="application/json", headers=[("sid", token)]
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(Sponsor.objects.count(), 0)
