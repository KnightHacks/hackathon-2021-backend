# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.hacker import Hacker
from src.models.user import User
from tests.base import BaseTestCase


class TestHackerModel(BaseTestCase):
    """Tests for the Hacker Model"""

    def test_create_hacker(self):
        hacker = Hacker.createOne(
            email="foobar@email.com",
            mlh=dict(
                mlh_code_of_conduct=True,
                mlh_privacy_and_contest_terms=True
            )
        )

        self.assertTrue(hacker.id)
        self.assertEqual(hacker.email, "foobar@email.com")

