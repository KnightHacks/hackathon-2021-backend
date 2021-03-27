# flake8: noqa
import json
from src.models.category import Category
from tests.base import BaseTestCase


class TestCategoriesBlueprint(BaseTestCase):
    """Tests for the categories Endpoints"""

    """create_category"""

    def test_create_category(self):
        pass

    def test_create_category_invalid_json(self):
        pass

    def test_create_category_sponsor_not_found(self):
        pass

    def test_create_category_duplicate_category(self):
        pass

    def test_create_category_invalid_datatypes(self):
        pass

    """edit_category"""

    def test_edit_category(self):
        pass

    def test_edit_category_sponsor_not_found_query(self):
        pass

    def test_edit_category_not_found(self):
        pass

    def test_edit_category_sponsor_not_found_update(self):
        pass

    def test_edit_category_duplicate_category(self):
        pass

    def test_edit_category_invalid_datatypes(self):
        pass

    """delete_category"""

    def test_delete_category(self):
        pass

    def test_delete_category_sponsor_not_found(self):
        pass

    def test_delete_category_not_found(self):
        pass

    """get_category"""

    def test_get_category(self):
        pass

    def test_get_category_sponsor_not_found(self):
        pass

    def test_get_category_not_found(self):
        pass
