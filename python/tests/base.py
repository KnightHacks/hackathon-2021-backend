# flake8: noqa
import os, json
from flask_testing import TestCase
from mongoengine import connect
from mongoengine.connection import disconnect_all
from src.models.user import User, ROLES

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

    def login_user(self, roles: ROLES):
        user = User.createOne(username="tester",
                       email="tester@localhost.dev",
                       password="123456",
                       roles=roles)

        token = user.encode_auth_token()

        return token
