from accounts.groups import GROUP_MANAGERS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_and_username_only(self):
        user = User(username="Jean-Claude", email='a@b.com')
        user.full_clean()  # should not raise

    def test_has_id_as_is_primary_key(self):
        user = User()
        self.assertTrue(hasattr(user, 'id'))

    def test_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated())

    def test_add_user_to_group(self):
        user = User.objects.create(email="a@b.com")
        group = Group.objects.get(name=GROUP_MANAGERS)
        user.add_to_group("Test group")
        print(user.groups)
        self.assertIn(
            group,
            user.groups
        )
