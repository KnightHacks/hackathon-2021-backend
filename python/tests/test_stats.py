# flake8: noqa
import json
from src.models.hacker import Hacker
from tests.base import BaseTestCase


class TestStatsBlueprint(BaseTestCase):
    """Tests for the Stats Endpoints"""

    def test_user_count(self):

        res = self.client.get("/api/stats/user_count/", headers=[("Accept", "application/json")])
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 200)

        self.assertEqual(data["hackers"], 0)
        self.assertEqual(data["total"], 0)
