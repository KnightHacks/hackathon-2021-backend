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
                    "mlh": {
                        "mlh_code_of_conduct": True,
                        "mlh_privacy_and_contest_terms": True
                    }
                }
            )},
            content_type="multipart/form-data",
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Hacker.objects.count(), 1)

    def test_create_hacker_not_accepted_mlh_coc(self):
        res = self.client.post(
            "/api/hackers/",
            data=json.dumps({
                "email": "foobar@email.com",
                "mlh": {
                    "mlh_code_of_conduct": False,
                    "mlh_privacy_and_contest_terms": True
                }
            }),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 422)
        self.assertEqual(Hacker.objects.count(), 0)

        res = self.client.post(
            "/api/hackers/",
            data=json.dumps({
                "email": "foobar@email.com",
                "mlh": {
                    "mlh_privacy_and_contest_terms": True
                }
            }),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 422)
        self.assertEqual(Hacker.objects.count(), 0)

    def test_create_hacker_not_accepted_mlh_pact(self):
        res = self.client.post(
            "/api/hackers/",
            data=json.dumps({
                "email": "foobar@email.com",
                "mlh": {
                    "mlh_code_of_conduct": True,
                    "mlh_privacy_and_contest_terms": False
                }
            }),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 422)
        self.assertEqual(Hacker.objects.count(), 0)

        res = self.client.post(
            "/api/hackers/",
            data=json.dumps({
                "email": "foobar@email.com",
                "mlh": {
                    "mlh_code_of_conduct": True
                }
            }),
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 422)
        self.assertEqual(Hacker.objects.count(), 0)

    def test_create_hacker_extraneous_fields(self):

        res = self.client.post(
            "/api/hackers/",
            data=json.dumps({
                "email": "foobar@email.com",
                "mlh": {
                    "mlh_code_of_conduct": True,
                    "mlh_privacy_and_contest_terms": True
                },
                "edu_info": {
                    "extrabs": "asdf"
                }
            }),
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 418)
        self.assertEqual(Hacker.objects.count(), 0)


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
                    "mlh": {
                        "mlh_code_of_conduct": True,
                        "mlh_privacy_and_contest_terms": True
                    }
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
            data={"hacker": json.dumps(
                {"email": "notanemail",
                 "mlh": {
                     "mlh_code_of_conduct": True,
                     "mlh_privacy_and_contest_terms": True
                 }}
            )},
            content_type="multipart/form-data",
        )

        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["name"], "Bad Request")
        self.assertEqual(Hacker.objects.count(), 0)

    """get_all_hackers"""
    def test_get_all_hackers(self):
        Hacker.createOne(
            email="foobar@email.com",
            mlh=dict(
                mlh_code_of_conduct=True,
                mlh_privacy_and_contest_terms=True
            )
        )

        Hacker.createOne(
            email="foobar1@email.com",
            mlh=dict(
                mlh_code_of_conduct=True,
                mlh_privacy_and_contest_terms=True
            )
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
