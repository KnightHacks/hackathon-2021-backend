# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.user import User
from tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    """Tests for the User Model"""

    def test_create_user(self):
        user = User.createOne(username="foobar",
                        email="foobar@email.com",
                        password="password",
                        roles=("HACKER",))

        self.assertTrue(user.id)
        self.assertEqual(user.username, "foobar")
        self.assertEqual(user.email, "foobar@email.com")
        self.assertTrue(user.password)
