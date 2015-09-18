from django.db import IntegrityError

from core.tests.base import CoreTestCase
from core.models.users import AgripoUser as User


class FarmerModelTest(CoreTestCase):

    def test_simple_user_is_not_a_farmer(self):
        user = User(username="Jean-Claude", password="my_pass", email="mail@dom.net")
        user.save()
        self.assertFalse(user.is_farmer())

    def test_add_user_to_farmers_group(self):
        user = User(username="Jean-Claude", password="my_pass", email="mail@dom.net")
        user.save()
        user.add_to_farmers()
        self.assertTrue(user.is_farmer())

    def test_farmer_must_have_email(self):
        user = User(username="Jean-Claude", password="my_pass")
        user.save()
        self.assertRaises(IntegrityError, user.add_to_farmers)
