# flake8: noqa
import json
from src.models.sponsor import Sponsor
from tests.base import BaseTestCase


class TestSponsorsBlueprint(BaseTestCase):
    """Tests for the Sponsors Endpoints"""

    """create_sponsor"""
    def test_create_sponsor(self):
        pass

    def test_create_sponsor_invalid_json(self):
        pass

    def test_create_sponsor_duplicate_sponsor(self):
        pass

    def test_create_sponsor_invalid_datatypes(self):
        pass
