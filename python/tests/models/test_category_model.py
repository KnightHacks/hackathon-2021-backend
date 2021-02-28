# flake8: noqa
from mongoengine.errors import NotUniqueError
from src.models.sponsor import Sponsor
from src.models.category import Category
from tests.base import BaseTestCase


class TestCategoryModel(BaseTestCase):
    """Tests for the Category Model"""

    def test_create_category(self):
        sponsor = Sponsor.createOne(username="foobar",
                                    email="foobar@foobar.com",
                                    password="pluto is a planet",
                                    roles=("SPONSOR",))

        category = Category.createOne(name="foobar",
                                      description="Lorem ipsum",
                                      sponsor=sponsor)

        self.assertTrue(category.id)
        self.assertEqual(category.sponsor, sponsor)
        self.assertEqual(category.name, "foobar")
        self.assertEqual(category.description, "Lorem ipsum")
