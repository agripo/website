from core.views import NUMBER_OF_NEWS_BY_PAGE
from django.core.urlresolvers import reverse
from django.test import TestCase
import datetime

from core.authentication import force_production_server
from core.models import AgripoUser as User, News


class CoreTestCase(TestCase):

    def tearDown(self):
        # We reset the session to the default (dev/staging/prod) server
        force_production_server(False)

    def auto_connect(self, email):
        return self.client.get('/core/auto_login/{}'.format(email))

    def auto_manager_connect(self, email):
        return self.client.get('/core/auto_manager_login/{}'.format(email))


class LoginViewTest(CoreTestCase):

    def test_can_auto_connect_with_new_email(self):
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "{} is connected as user".format('alpha@test.com'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_can_auto_connect_as_manager_with_new_email(self):
        page = self.auto_manager_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "{} is connected as manager".format('alpha@test.com'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_cant_auto_connect_with_existing_email(self):
        User.objects.create(email="alpha@test.com")
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "No autoconnection with existing user")
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_cant_auto_connect_on_production_server(self):
        force_production_server(True)  # deactivation is made in TearDown
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "No autoconnection on production server")
        self.assertNotIn('_auth_user_id', self.client.session)


class NewsViewsTest(CoreTestCase):

    def create_writer_if_none(self, writer):
        if not writer:
            writer = User.objects.create(username="Writer Boy", email="writer@mail.com", password="")
        return writer

    def insert_news(self, title, content, writer=None, publication_date=None):
        writer = self.create_writer_if_none(writer)
        if not publication_date:
            # We define it in the past
            publication_date = datetime.datetime.now() - datetime.timedelta(10)
        return News.objects.create(title=title, content=content, writer=writer, publication_date=publication_date)

    def insert_x_news(self, number, title, content, writer=None, publication_date=None):
        writer = self.create_writer_if_none(writer)
        for i in range(0, number):
            self.insert_news(title.format(i), content.format(i), writer, publication_date=publication_date)

    def test_display_all_news_if_less_than_pagination(self):
        self.insert_x_news(NUMBER_OF_NEWS_BY_PAGE, "News #{}", "Content for #{}")
        response = self.client.get(reverse('news_page'))
        self.assertContains(response, "News #{}".format(0))
        self.assertContains(response, "News #{}".format(NUMBER_OF_NEWS_BY_PAGE - 1))

    def test_display_max_news_if_more_than_pagination(self):
        self.insert_x_news(NUMBER_OF_NEWS_BY_PAGE + 5, "One news title", "Content for #{}")
        response = self.client.get(reverse('news_page'))
        self.assertContains(response, "One news title", NUMBER_OF_NEWS_BY_PAGE)

    def fill_with_entries_and_get_page(self, page_num=1):
        writer = self.create_writer_if_none(None)
        for i in range(0, NUMBER_OF_NEWS_BY_PAGE + 10):
            pub = datetime.datetime.now() - datetime.timedelta(i - 5)
            self.insert_news("News #{}".format(i), "content", writer, publication_date=pub)

        return self.client.get(reverse('news_page') + "?page=" + str(page_num))

    def test_display_recent_entries(self):
        response = self.fill_with_entries_and_get_page()
        for i in range(5, NUMBER_OF_NEWS_BY_PAGE + 5):
            self.assertContains(response, "News #{}".format(i))

    def test_future_entries(self):
        response = self.fill_with_entries_and_get_page()
        self.assertNotContains(response, "News #{}".format(4))

    def test_hide_older_entries_from_front_page(self):
        response = self.fill_with_entries_and_get_page()
        self.assertNotContains(response, "News #{}".format(5 + NUMBER_OF_NEWS_BY_PAGE))

    def test_display_older_posts_on_following_pagination_pages(self):
        response = self.fill_with_entries_and_get_page(2)
        self.assertContains(response, "News #{}".format(5 + NUMBER_OF_NEWS_BY_PAGE))
