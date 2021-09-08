# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.hacker import Hacker
from src.models.user import User
from tests.base import BaseTestCase


class TestHackerModel(BaseTestCase):
    """Tests for the Hacker Model"""

    def test_create_hacker(self):
        hacker = Hacker.createOne(
            email="foobar@email.com"
        )

        self.assertTrue(hacker.id)
        self.assertEqual(hacker.email, "foobar@email.com")

