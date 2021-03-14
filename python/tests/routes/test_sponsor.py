# flake8: noqa
import json
from src.models.sponsor import Sponsor
from tests.base import BaseTestCase
from src.models.user import ROLES


class TestSponsorsBlueprint(BaseTestCase):
    """Tests for the Sponsors Endpoints"""

    """create_sponsor"""
    def test_create_sponsor(self):
        pass

    def test_create_sponsor_invalid_json(self):
        pass

    def test_create_sponsor_duplicate_sponsor(self):
        pass

    def test_create_sponsor_invalid_datatypes(self):
        pass

    """delete_sponsor"""
    def test_delete_sponsor(self):
        Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        token = self.login_user(ROLES.ADMIN)

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_delete_sponsor_as_self(self):
        sponsor = Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        token = sponsor.encode_auth_token()

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Sponsor.objects.count(), 0)

    def test_delete_sponsor_as_other_sponsor(self):
        Sponsor.createOne(username="foobar",
                          sponsor_name="foobar",
                          email="foobar@email.com",
                          password="123456",
                          roles=ROLES.SPONSOR)

        other_sponsor = Sponsor.createOne(username="tester",
                                          sponsor_name="tester",
                                          email="tester@email.com",
                                          password="123456",
                                          roles=ROLES.SPONSOR)

        token = other_sponsor.encode_auth_token()

        res = self.client.delete("/api/sponsors/delete_sponsor/foobar/",
                                 headers=[("sid", token)])

        self.assertEqual(res.status_code, 401)

    def test_delete_sponsor_not_found(self):
        pass
