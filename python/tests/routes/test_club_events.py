# flake8: noqa
import json
from src.models.club_event import ClubEvent
from tests.base import BaseTestCase


class TestClubEventsBlueprint(BaseTestCase):
    """Tests for the Club Events Endpoints"""

    """update_events"""
    def test_update_events(self):
        pass

    def test_update_events_invalid_json(self):
        pass

    def test_update_events_invalid_datatypes(self):
        pass

    """get_events"""
    def test_get_events(self):
        pass

    def test_get_events_mix_rdate_startend_dates(self):
        pass

    def test_get_events_confirmed_with_dates(self):
        pass

    def test_get_events_rdate_today(self):
        pass

    def test_get_events_rdate_nextweek(self):
        pass

    def test_get_events_rdate_nextmonth(self):
        pass

    def test_get_events_rdate_nextyear(self):
        pass
