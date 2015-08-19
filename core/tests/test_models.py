from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from core.models import AgripoUser as User, News
import datetime


class UserModelTest(TestCase):

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


class MockToday(datetime.date):

    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


class NewsModelTest(TestCase):

    def _create_user(self, username="Jean-Claude"):
        return User.objects.create(username=username, password="my_pass")

    def _create_news(self, user=None, save=True, in_the_past=False):
        if not user:
            user = self._create_user().add_to_managers()

        if in_the_past:
            original_datetime = datetime.date
            datetime.date = MockToday

        news = News(title="Some random title", content="And some random content", writer=user)
        if save:
            news.save()
        else:
            news.full_clean()

        if in_the_past:
            datetime.date = original_datetime

        return news

    def test_manager_can_add_news(self):
        user = self._create_user().add_to_managers()
        self._create_news(user, False)  # should not raise

    def test_cant_publish_two_news_at_the_same_time(self):
        user = self._create_user().add_to_managers()
        pub = datetime.date.today() - datetime.timedelta(1)
        n = News(title="Title", content="Content", writer=user, publication_date=pub)
        n.save()
        n2 = News(title="Title", content="Content", writer=user, publication_date=pub)
        self.assertRaises(IntegrityError, n2.save)

    def test_manager_also_admin_can_add_news(self):
        user = self._create_user().add_to_managers().add_to_admins()
        self._create_news(user, False)  # should not raise

    def test_other_users_and_anonymous_cant_add_news(self):
        user = self._create_user()
        self.assertRaises(ValidationError, self._create_news, user, False)

    def test_manager_can_edit_news(self):
        pass

    def test_other_users_and_anonymous_cant_edit_news(self):
        pass

    def test_manager_can_delete_news(self):
        pass

    def test_other_users_and_anonymous_cant_delete_news(self):
        pass

    def test_new_entry_created_with_good_creation_date(self):
        today = datetime.date.today()
        news = self._create_news()
        self.assertEqual(news.creation_date, today)

    def test_get_edition_date_returns_none_for_new_entries(self):
        news = self._create_news()
        self.assertIsNone(news.get_edition_date())

    def test_edited_entry_creation_date_didn_t_change(self):
        news = self._create_news(in_the_past=True)
        original_creation_date = news.creation_date

        news.title = "Updated title"
        news.save()

        self.assertEqual(news.creation_date, original_creation_date)

    def test_edited_entry_edited_date_changed(self):
        news = self._create_news(in_the_past=True)
        original_edition_date = news.edition_date

        news.title = "Updated title"
        news.save()

        self.assertNotEqual(news.edition_date, original_edition_date)

    def test_news_without_pubdate_are_published_at_that_moment(self):
        before = timezone.now()
        news = self._create_news()
        after = timezone.now()
        self.assertGreater(news.publication_date, before)
        self.assertLess(news.publication_date, after)

    def test_news_can_have_an_icon(self):
        user = self._create_user().add_to_managers()
        pub = datetime.date.today() - datetime.timedelta(1)
        n = News(title="Title", content="Content", writer=user, publication_date=pub, icon="star")
        n.save()  # should not raise

    def test_news_icon_defaults_to_(self):
        user = self._create_user().add_to_managers()
        pub = datetime.date.today() - datetime.timedelta(1)
        n = News(title="Title", content="Content", writer=user, publication_date=pub)
        n.save()  # should not raise
        self.assertEqual(n.icon, 'comment')

    #@todo: check that the Icons model contains the icons
