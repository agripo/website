import random
import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from core.tests.views.base import ViewsBaseTestCase
from core.models.news import News
from core.models.general import Icon
from core.models.users import AgripoUser as User
from core.data.icons import UNUSED_ICON


class NewsViewsTest(ViewsBaseTestCase):

    def create_writer_if_none(self, writer):
        if not writer:
            writer = User.objects.create(username="Writer Boy", email="writer@mail.com", password="")
        return writer

    def insert_news(self, title, content, writer=None, publication_date=None, icon=None):
        writer = self.create_writer_if_none(writer)
        if not publication_date:
            # We define it in the past
            publication_date = timezone.now() - datetime.timedelta(10)
        if not icon:
            random_idx = random.randint(0, Icon.objects.count() - 1)
            icon = Icon.objects.all()[random_idx]
        return News.objects.create(
            title=title, content=content, writer=writer, publication_date=publication_date, icon=icon)

    def insert_x_news(self, number, title, content, writer=None, publication_date=None):
        writer = self.create_writer_if_none(writer)
        for i in range(0, number):
            self.insert_news(title.format(i), content.format(i), writer, publication_date=publication_date)

    def test_display_all_news_if_less_than_pagination(self):
        number_of_news = self.config.news_count
        self.insert_x_news(number_of_news, "News #{}", "Content for #{}")
        response = self.client.get(reverse('news_page'))
        self.assertContains(response, "News #{}".format(0))
        self.assertContains(response, "News #{}".format(number_of_news - 1))

    def test_display_max_news_if_more_than_pagination(self):
        number_of_news = self.config.news_count
        self.insert_x_news(number_of_news + 5, "One news title", "Content for #{}")
        response = self.client.get(reverse('news_page'))
        self.assertContains(response, 'One news title', number_of_news)

    def fill_with_entries(self, entries_count=0):
        if entries_count == 0:
            entries_count = self.config.news_count + 10

        writer = self.create_writer_if_none(None)
        for i in range(1, entries_count + 1):
            pub = timezone.now() - timezone.timedelta(i - 5)
            icon = Icon.objects.get(pk=i)
            self.insert_news("News #{}".format(i), "content", writer, publication_date=pub, icon=icon)

    def fill_with_entries_and_get_page(self, page_num=1):
        self.fill_with_entries()
        return self.client.get(reverse('news_page') + "?page=" + str(page_num))

    def test_display_recent_entries(self):
        number_of_news = self.config.news_count
        response = self.fill_with_entries_and_get_page()
        for i in range(5, number_of_news + 5):
            self.assertContains(response, "News #{}".format(i))

    def test_future_entries(self):
        response = self.fill_with_entries_and_get_page()
        self.assertNotContains(response, "News #{}".format(4))

    def test_hide_older_entries_from_front_page(self):
        number_of_news = self.config.news_count
        response = self.fill_with_entries_and_get_page()
        self.assertNotContains(response, "News #{}".format(6 + number_of_news))

    def test_display_older_posts_on_following_pagination_pages(self):
        number_of_news = self.config.news_count
        response = self.fill_with_entries_and_get_page(2)
        self.assertContains(response, "News #{}".format(6 + number_of_news))

    def test_context_contains_reference_to_older_entry(self):
        self.fill_with_entries(5)
        response = self.client.get(reverse('one_news_page', kwargs={'pk': 3}))
        self.assertContains(response, 'href="{}"'.format(reverse('one_news_page', kwargs={'pk': 2})))

    def test_icon_is_found_on_news_page_in_title(self):
        self.fill_with_entries(10)
        # Using the tenth to be sure not to find the icon in other modules
        news = News.objects.get(pk=10)
        news.icon = Icon.objects.get(icon=UNUSED_ICON)
        news.save()
        response = self.client.get(reverse('one_news_page', kwargs={'pk': 10}))
        self.assertContains(
            response, '<i class="fa fa-{}"></i>'.format(UNUSED_ICON))
