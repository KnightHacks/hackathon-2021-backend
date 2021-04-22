# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.team import Team
from src.models.hacker import Hacker
from src.models.user import User, ROLES
from tests.base import BaseTestCase
from datetime import datetime


class TestTeamModel(BaseTestCase):
    """Tests for the Team Model"""

    def test_create_team(self):
        hacker = Hacker.createOne(
            username="foobar",
            email="foobar@email.com",
            password="password",
            roles=ROLES.HACKER,
        )

        now = datetime.now()
        team = Team.createOne(
            name="foobar", icon="image", categories=["cat1"], date=now, members=[hacker]
        )

        self.assertTrue(team.id)
        self.assertEqual(team.name, "foobar")
        self.assertEqual(team.icon, "image")
        self.assertEqual(team.categories, ["cat1"])
        self.assertEqual(team.date, now)
        self.assertEqual(team.members[0], hacker)

    def test_team_to_json(self):
        hacker = Hacker.createOne(
            username="foobar",
            email="foobar@email.com",
            password="password",
            first_name="foo",
            last_name="bar",
            roles=ROLES.HACKER,
        )

        now = datetime.now()
        team = Team.createOne(
            name="foobar", icon="image", categories=["cat1"], date=now, members=[hacker]
        )

        team_json = team.to_mongo().to_dict()

        self.assertEqual("foobar", team_json["name"])
        self.assertEqual("image", team_json["icon"])
        self.assertEqual(["cat1"], team_json["categories"])
        self.assertEqual(now, team_json["date"])
