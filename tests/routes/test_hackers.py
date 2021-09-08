# flake8: noqa
import json
from src.models.hacker import Hacker
from tests.base import BaseTestCase
from datetime import datetime


class TestHackersBlueprint(BaseTestCase):
    """Tests for the Hackers Endpoints"""

    """create_hacker"""

    def test_create_hacker(self):
        now = datetime.now()
        res = self.client.post(
            "/api/hackers/",
            data={"hacker": json.dumps(
                {
                    "email": "foobar@email.com",
                    "date": now.isoformat(),
                }
            )},
            content_type="multipart/form-data",
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 1)

    def test_create_hacker_invalid_json(self):
        res = self.client.post(
            "/api/hackers/", data={"hacker": ""}, content_type="multipart/form-data"
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")
        self.assertEqual(Hacker.objects.count(), 0)

    def test_create_hacker_duplicate_user(self):
        now = datetime.now()
        Hacker.createOne(
            email="foobar@email.com"
        )

        res = self.client.post(
            "/api/hackers/",
            data={"hacker": json.dumps(
                {
                    "email": "foobar@email.com",
                    "date": now.isoformat(),
                }
            )},
            content_type="multipart/form-data",
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 409)
        self.assertIn(
            "Sorry, that email already exists.", data["description"]
        )
        self.assertEqual(Hacker.objects.count(), 1)

    def test_create_hacker_invalid_datatypes(self):
        res = self.client.post(
            "/api/hackers/",
            data=json.dumps(
                {"email": "notanemail"}
            ),
            content_type="application/json",
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")
        self.assertEqual(Hacker.objects.count(), 0)

    """get_all_hackers"""
    def test_get_all_hackers(self):
        Hacker.createOne(
            email="foobar@email.com"
        )

        Hacker.createOne(
            email="foobar1@email.com",
        )

        token = self.login_user()

        res = self.client.get("/api/hackers/get_all_hackers/", 
                              headers=[("sid", token)])

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["hackers"][0]["email"], "foobar@email.com")
        self.assertEqual(data["hackers"][1]["email"], "foobar1@email.com")

    
    def test_get_all_hackers_not_found(self):
        token = self.login_user()

        res = self.client.get("/api/hackers/get_all_hackers/", 
                              headers=[("sid", token)])

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["name"], "Not Found")
