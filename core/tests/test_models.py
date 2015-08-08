from core.groups import GROUP_MANAGERS
from django.contrib.auth.models import Group
from django.test import TestCase

from core.models import AgripoUser as User

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_username_and_password_only(self):
        user = User(username="Jean-Claude", email='a@b.com', password="my_pass")
        user.full_clean()  # should not raise

    def test_has_id_as_is_primary_key(self):
        user = User()
        self.assertTrue(hasattr(user, 'id'))

    def test_is_authenticated(self):
        # is_authenticated always return True to make a difference between User instances and AnonymousUser
        user = User()
        self.assertTrue(user.is_authenticated())

    def test_add_user_to_group(self):
        user = User.objects.create(username="Jean-Claude", password="my_pass")
        user.add_to_group(GROUP_MANAGERS)
        self.assertEqual(
            user.groups.all()[0].name,
            GROUP_MANAGERS
        )
