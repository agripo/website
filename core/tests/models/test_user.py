from core.tests.base import CoreTestCase
from core.models.users import AgripoUser as User


class UserModelTest(CoreTestCase):

    def test_add_to_managers_returns_user(self):
        user = User(username="Jean-Claude", password="my_pass").add_to_managers()
        self.assertIsInstance(user, User)

    def test_add_to_managers_hits_db(self):
        User(username="Jean-Claude", password="my_pass").add_to_managers()
        user = User.objects.get(username="Jean-Claude")
        self.assertTrue(user.is_manager)

    def test_add_to_admins_returns_user(self):
        user = User(username="Jean-Claude", password="my_pass").add_to_admins()
        self.assertIsInstance(user, User)

    def test_add_to_admins_hits_db(self):
        User(username="Jean-Claude", password="my_pass").add_to_admins()
        user = User.objects.get(username="Jean-Claude")
        self.assertTrue(user.is_admin)

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

    def test_new_manager_is_viewed_as_such(self):
        user = User.objects.create(username="Jean-Claude", password="my_pass")
        user.add_to_managers()
        self.assertTrue(user.is_manager())

    def test_new_admin_is_viewed_as_such(self):
        user = User.objects.create(username="Jean-Claude", password="my_pass")
        user.add_to_admins()
        self.assertTrue(user.is_admin())

