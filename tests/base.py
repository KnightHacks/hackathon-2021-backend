# flake8: noqa
import os, json
from flask_testing import TestCase
from mongoengine import connect
from mongoengine.connection import disconnect_all
from src.models.user import User, ROLES
from src.models.tokenblacklist import TokenBlacklist
from src.common.jwt import decode_jwt

os.environ["APP_SETTINGS"] = "src.config.TestingConfig"
from src import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object("src.config.TestingConfig")
        return app

    @classmethod
    def setUpClass(cls):
        disconnect_all()
        cls._conn = connect("mongoenginetest", host="mongomock://localhost")
        cls._conn.drop_database("mongoenginetest")

    @classmethod
    def tearDownClass(cls):
        cls._conn.drop_database("mongoenginetest")
        disconnect_all()

    def tearDown(self):
        self._conn.drop_database("mongoenginetest")

    def login_as(self, user: User, password: str) -> str:
        login = self.client.post(
            "/api/auth/login/",
            data=json.dumps({
                "username": user.username,
                "password": password
            }),
            content_type="application/json"
        )

        return login.headers["Set-Cookie"][4:-8]

    def login_user(self, roles: ROLES):
        user = User.createOne(
            username="tester",
            email="tester@localhost.dev",
            password="123456",
            roles=roles
        )

        token = user.encode_auth_token()

        decoded_token = decode_jwt(token)

        """ Add token to Token Blacklist as a non-revoked token """
        TokenBlacklist.createOne(
            jti=decoded_token["jti"],
            user=user
        )

        return token
