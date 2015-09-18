import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from core.tests.base import CoreTestCase
from core.models.news import News
from core.models.general import Icon
from core.models.users import AgripoUser as User


class MockToday(datetime.date):

    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


class NewsModelTest(CoreTestCase):

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
        icon = Icon.objects.get(icon="star")
        n = News(title="Title", content="Content", writer=user, publication_date=pub, icon=icon)
        n.save()  # should not raise

    def test_news_icon_defaults_to_(self):
        user = self._create_user().add_to_managers()
        pub = datetime.date.today() - datetime.timedelta(1)
        n = News(title="Title", content="Content", writer=user, publication_date=pub)
        n.save()  # should not raise
        icon = Icon.objects.get(icon="comment")
        self.assertEqual(n.icon, icon)

    # @todo: check that the Icons model contains the icons
