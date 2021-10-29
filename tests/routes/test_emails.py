# flake8: noqa
import json
from tests.base import BaseTestCase


class TestEmailsBlueprint(BaseTestCase):
    """Tests for the Emails Endpoints"""

    def test_check_verification_status(self):

        res = self.client.get(
            "/api/email/verify/foobar@email.com/",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(res.status_code, 410)


    def test_update_registration_status(self):

        res = self.client.get(
            "/api/email/verify/?token=foobar",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(res.status_code, 410)

    def test_send_verification_email(self):

        token = self.login_user()

        res = self.client.post(
            "/api/email/verify/foobar@email.com/",
            headers=[
                ("Accept", "application/json"),
                ("sid", token)
            ]
        )

        self.assertEqual(res.status_code, 410)
