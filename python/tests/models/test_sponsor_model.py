# flake8: noqa
from mongoengine.errors import NotUniqueError, ValidationError
from src.models.sponsor import Sponsor
from src.models.user import ROLES
from tests.base import BaseTestCase


class TestSponsorModel(BaseTestCase):
    """Tests for the Sponsor Model"""

    def test_create_sponsor(self):
        sponsor = Sponsor.createOne(username="foobar",
                        email="foobar@email.com",
                        password="password",
                        roles=ROLES.SPONSOR)

        self.assertTrue(sponsor.id)
        self.assertEqual(sponsor.username, "foobar")
        self.assertEqual(sponsor.email, "foobar@email.com")
        self.assertTrue(sponsor.password)
