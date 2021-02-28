# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.hacker import Hacker
from tests.base import BaseTestCase


class TestHackerModel(BaseTestCase):
    """Tests for the Hacker Model"""

    def test_create_hacker(self):
        hacker = Hacker.createOne(username="foobar",
                        email="foobar@email.com",
                        password="password",
                        roles=("HACKER",))

        self.assertTrue(hacker.id)
        self.assertEqual(hacker.username, "foobar")
        self.assertEqual(hacker.email, "foobar@email.com")
        self.assertTrue(hacker.password)
