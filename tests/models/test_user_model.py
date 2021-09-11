# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.user import User
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """Tests for the User Model"""

    def test_create_user(self):
        user = User.createOne(
            email="foobar@email.com"
        )

        self.assertTrue(user.id)
        self.assertEqual(user.email, "foobar@email.com")


    def test_findOne_user(self):
        User.createOne(
            email="foobar@email.com"
        )

        user = User.findOne(email="foobar@email.com")

        self.assertIsNone(user.id)
        self.assertEqual(user.email, "foobar@email.com")
