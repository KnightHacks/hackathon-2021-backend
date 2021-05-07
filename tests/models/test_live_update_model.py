# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.live_update import LiveUpdate
from tests.base import BaseTestCase
from datetime import datetime


class TestLiveUpdateModel(BaseTestCase):
    """Tests for the LiveUpdate Model"""

    def test_create_live_update(self):
        now = datetime.now()
        live_update = LiveUpdate.createOne(
            timestamp=now,
            message="Example Update message"
        )

        self.assertTrue(live_update.id)
        self.assertEqual(live_update.ID, 1)
        self.assertEqual(now, live_update.timestamp)
        self.assertEqual("Example Update message", live_update.message)
