# flake8: noqa
import json
from src.models.group import Group
from tests.base import BaseTestCase


class TestGroupsBlueprint(BaseTestCase):
    """Tests for the Groups Endpoints"""

    """create_group"""

    def test_create_group(self):
        pass

    def test_create_group_invalid_json(self):
        pass

    def test_create_group_member_not_found(self):
        pass

    def test_create_group_duplicate_group(self):
        pass

    def test_create_group_invalid_datatypes(self):
        pass

    """edit_group"""

    def test_edit_group(self):
        pass

    def test_edit_group_invalid_json(self):
        pass

    def test_edit_group_not_found(self):
        pass

    def test_edit_group_not_found_member(self):
        pass

    def test_edit_group_duplicate_group(self):
        pass

    def test_edit_group_invalid_datatypes(self):
        pass

    """get_group"""

    def test_get_group(self):
        pass

    def test_get_group_not_found(self):
        pass
