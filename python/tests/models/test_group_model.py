# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.group import Group
from src.models.hacker import Hacker
from tests.base import BaseTestCase
from datetime import datetime


class TestGroupModel(BaseTestCase):
    """Tests for the Group Model"""

    def test_create_group(self):
        hacker = Hacker.createOne(username="foobar",
                        email="foobar@email.com",
                        password="password",
                        roles=("HACKER",))

        now = datetime.now()
        group = Group.createOne(name="foobar",
                                icon="image",
                                categories=["cat1"],
                                date=now,
                                members=[hacker])

        self.assertTrue(group.id)
        self.assertEqual(group.name, "foobar")
        self.assertEqual(group.icon, "image")
        self.assertEqual(group.categories, ["cat1"])
        self.assertEqual(group.date, now)
        self.assertEqual(group.members[0], hacker)

    def test_group_to_json(self):
        hacker = Hacker.createOne(username="foobar",
                                  email="foobar@email.com",
                                  password="password",
                                  first_name="foo",
                                  last_name="bar",
                                  roles=("HACKER",))

        now = datetime.now()
        group = Group.createOne(name="foobar",
                                icon="image",
                                categories=["cat1"],
                                date=now,
                                members=[hacker])

        group_json = group.to_json()

        self.assertEqual("foobar", group_json["name"])
        self.assertEqual("image", group_json["icon"])
        self.assertEqual(["cat1"], group_json["categories"])
        self.assertEqual(now, group_json["date"])
        self.assertIn({
            "first_name": hacker.first_name,
            "last_name": hacker.last_name,
            "email": hacker.email,
            "username": hacker.username
        }, group_json["members"])
