# flake8: noqa
import json
from tests.base import BaseTestCase


class TestFlasgger(BaseTestCase):
    """Tests to ensure that Flasgger is functioning properly"""

    def test_get_apidocs(self):
        """The GET on /apidocs should return 200"""

        res = self.client.get("/apidocs/")

        self.assertEqual(res.status_code, 200)

    def test_flasgger_is_not_empty(self):
        """The GET on /apispec.json should return a dict with a non-empty paths prop"""

        res = self.client.get("/apispec.json")
        data = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["paths"])
