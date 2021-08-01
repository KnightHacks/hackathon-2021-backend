# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.hacker import Hacker
from src.models.user import User, ROLES
from src.models.tokenblacklist import TokenBlacklist
from tests.base import BaseTestCase


class TestHackerModel(BaseTestCase):
    """Tests for the Hacker Model"""

    def test_create_hacker(self):
        hacker = Hacker.createOne(
            username="foobar",
            email="foobar@email.com",
            password="password",
            roles=ROLES.HACKER,
        )

        self.assertTrue(hacker.id)
        self.assertEqual(hacker.username, "foobar")
        self.assertEqual(hacker.email, "foobar@email.com")
        self.assertTrue(hacker.password)

    def test_delete_tokenblacklist(self):
        hacker = Hacker.createOne(
            username="foobar",
            email="foobar@email.com",
            password="password",
            roles=ROLES.HACKER,
        )

        self.login_as(hacker, password="password")

        self.assertEqual(TokenBlacklist.objects.count(), 1)

        hacker.delete()

        self.assertEqual(Hacker.objects.count(), 0)
        self.assertEqual(TokenBlacklist.objects.count(), 0)
