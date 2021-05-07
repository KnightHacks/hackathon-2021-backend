# flake8: noqa
import json
from tests.base import BaseTestCase
from src import app, socketio
from src.models.live_update import LiveUpdate
from src.models.user import ROLES


class TestLiveUpdatesBlueprint(BaseTestCase):
    """Tests for the LiveUpdates Endpoints"""

    def setUp(self):
        super().tearDown()
        self.wsclient = socketio.test_client(
            app,
            flask_test_client=self.client
        )

    def tearDown(self):
        super().tearDown()
        self.wsclient.disconnect()

    """wss on_connect hello"""
    def test_on_connect_empty(self):

        self.wsclient.connect(
            namespace="/liveupdates"
        )

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(ws_resc[0].get("name"), "hello")
        self.assertEqual(ws_resc[0].get("args")[0], [])

    def test_on_connect_not_empty(self):

        LiveUpdate.createOne(message="Testing my dude")
        LiveUpdate.createOne(message="Testing my dude 2")

        self.wsclient.connect(
            namespace="/liveupdates"
        )

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(ws_resc[0].get("name"), "hello")
        ws_data = ws_resc[0].get("args")[0]

        self.assertEqual(len(ws_data), 2)
        self.assertIn("ID", ws_data[0])
        self.assertIn("timestamp", ws_data[0])
        self.assertIn(("message", "Testing my dude"), ws_data[0].items())

        self.assertIn("ID", ws_data[1])
        self.assertIn("timestamp", ws_data[1])
        self.assertIn(("message", "Testing my dude 2"), ws_data[1].items())

    """wss on_disconnect"""
    def test_on_disconnect(self):

        self.wsclient.connect(
            namespace="/liveupdates"
        )

        self.wsclient.disconnect(
            namespace="/liveupdates"
        )

    """wss on_reload"""
    def test_on_reload(self):

        self.wsclient.connect(
            namespace="/liveupdates"
        )
        self.wsclient.get_received(namespace="/liveupdates")

        LiveUpdate.createOne(message="Testing my dude")
        LiveUpdate.createOne(message="Testing my dude 2")

        self.wsclient.emit("reload",
                           namespace="/liveupdates")

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(len(ws_resc), 1)
        self.assertEqual(ws_resc[0].get("name"), "reload")

        ws_data = ws_resc[0].get("args")[0]

        self.assertEqual(len(ws_data), 2)
        self.assertIn("ID", ws_data[0])
        self.assertIn("timestamp", ws_data[0])
        self.assertIn(("message", "Testing my dude"), ws_data[0].items())

        self.assertIn("ID", ws_data[1])
        self.assertIn("timestamp", ws_data[1])
        self.assertIn(("message", "Testing my dude 2"), ws_data[1].items())

    """new_update"""
    def test_new_update(self):

        self.wsclient.connect(
            namespace="/liveupdates"
        )

        self.wsclient.get_received(namespace="/liveupdates")

        token = self.login_user(ROLES.ADMIN)

        res = self.client.put(
            "/api/live_updates/",
            data=json.dumps({
                "message": "Foobar is the message for today"
            }),
            headers=[("sid", token)],
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 201)

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(len(ws_resc), 1)
        self.assertEqual(ws_resc[0].get("name"), "NewLiveUpdate")
        self.assertEqual(len(ws_resc[0].get("args")), 1)

        ws_data = ws_resc[0].get("args")[0].get("data")

        self.assertEqual(ws_data.get("message"),
                         "Foobar is the message for today")

    def test_new_update_invalid_json(self):

        token = self.login_user(ROLES.ADMIN)

        res = self.client.put(
            "/api/live_updates/",
            data=json.dumps({}),
            headers=[("sid", token)],
            content_type="application/json"
        )

        self.assertEqual(res.status_code, 400)

    """delete_all_updates"""
    def test_delete_all_updates(self):
        LiveUpdate.createOne(message="Testing my dude")
        LiveUpdate.createOne(message="Testing my dude 2")

        self.wsclient.connect(namespace="/liveupdates")
        self.wsclient.get_received(namespace="/liveupdates")

        token = self.login_user(ROLES.ADMIN)

        self.client.delete(
            "/api/live_updates/all/",
            headers=[("sid", token)]
        )
        self.assertEqual(LiveUpdate.objects.count(), 0)

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(ws_resc[0].get("name"), "DeleteAllLiveUpdates")

    """delete_update"""
    def test_delete_update(self):
        LiveUpdate.createOne(message="Testing my dude")
        second = LiveUpdate.createOne(message="Testing my dude 2")

        self.wsclient.connect(namespace="/liveupdates")
        self.wsclient.get_received(namespace="/liveupdates")

        token = self.login_user(ROLES.ADMIN)

        self.client.delete(
            "/api/live_updates/1/",
            headers=[("sid", token)]
        )
        self.assertEqual(LiveUpdate.objects.count(), 1)
        self.assertIsNone(LiveUpdate.objects(ID=1).first())
        self.assertEqual(LiveUpdate.objects.first(), second)

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(ws_resc[0].get("name"), "DeleteLiveUpdate")
        self.assertEqual(ws_resc[0]["args"][0]["data"], "1")

    def test_delete_update_not_found(self):
        LiveUpdate.createOne(message="Testing my dude")
        second = LiveUpdate.createOne(message="Testing my dude 2")

        self.wsclient.connect(namespace="/liveupdates")
        self.wsclient.get_received(namespace="/liveupdates")

        token = self.login_user(ROLES.ADMIN)

        res = self.client.delete(
            "/api/live_updates/3/",
            headers=[("sid", token)]
        )
        self.assert404(res)
        self.assertEqual(LiveUpdate.objects.count(), 2)

        ws_resc = self.wsclient.get_received(namespace="/liveupdates")

        self.assertEqual(ws_resc, [])
