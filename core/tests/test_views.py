from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
import datetime
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

from core.authentication import force_production_server
from core.models import AgripoUser as User, News, SiteConfiguration, Product
from core.management.commands.populatedb import (
    insert_random_categories_and_products, insert_random_category)


config = SiteConfiguration.objects.get()
NUMBER_OF_NEWS_BY_PAGE = config.news_count


class CoreTestCase(TestCase):

    def setUp(self):
        # We add a SocialApp as we get an error if it's not done
        app = SocialApp(pk=1, provider="facebook", name="Facebook", client_id="001122334455667",
                        secret="00112233445566778899aabbccddeeff")
        app.sites.add(Site.objects.get_current().id)
        app.save()

    def tearDown(self):
        # We reset the session to the default (dev/staging/prod) server
        force_production_server(False)

    def auto_connect(self, email):
        return self.client.get('/core/auto_login/{}'.format(email))

    def auto_manager_connect(self, email):
        return self.client.get('/core/auto_manager_login/{}'.format(email))


class ShopViewTest(CoreTestCase):

    def _shop_page_contains(self, text, quantity):
        response = self.client.get(reverse('shop_page'))
        self.assertContains(response, text, quantity)

    def test_use_template(self):
        response = self.client.get(reverse('shop_page'))
        self.assertTemplateUsed(response, 'core/shop_page.html')

    def test_display_all_products(self):
        insert_random_categories_and_products(5, 4)
        self._shop_page_contains('class="one_product"', 20)

    def test_display_message_for_products_out_of_stock(self):
        self.fail("Test not implemented yet")

    def test_display_all_categories(self):
        insert_random_categories_and_products(5, 0)
        self._shop_page_contains('class="one_product_category"', 5)

    def test_display_message_for_empty_categories(self):
        insert_random_categories_and_products(2, 1)
        insert_random_categories_and_products(2, 0)
        self._shop_page_contains('class="one_product_category_empty"', 2)

    def test_prefill_quantity_from_cart(self):
        insert_random_categories_and_products(2, 2)
        prod = Product.objects.get(pk=1)
        prod.set_cart_quantity(2)
        self._shop_page_contains('<span>{} unités</span>'.format(2), 1)


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
            publication_date = timezone.now() - datetime.timedelta(10)
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
        self.assertContains(response, 'One news title', NUMBER_OF_NEWS_BY_PAGE + 3)  # There are 3 boxes in the bottom module

    def fill_with_entries(self, entries_count=NUMBER_OF_NEWS_BY_PAGE + 10):
        writer = self.create_writer_if_none(None)
        for i in range(1, entries_count + 1):
            pub = timezone.now() - timezone.timedelta(i - 5)
            self.insert_news("News #{}".format(i), "content", writer, publication_date=pub)

    def fill_with_entries_and_get_page(self, page_num=1):
        self.fill_with_entries()
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
        self.assertNotContains(response, "News #{}".format(6 + NUMBER_OF_NEWS_BY_PAGE))

    def test_display_older_posts_on_following_pagination_pages(self):
        response = self.fill_with_entries_and_get_page(2)
        self.assertContains(response, "News #{}".format(6 + NUMBER_OF_NEWS_BY_PAGE))

    def test_context_contains_reference_to_older_entry(self):
        self.fill_with_entries(5)
        response = self.client.get(reverse('one_news_page', kwargs={'pk': 3}))
        self.assertContains(response, 'href="{}"'.format(reverse('one_news_page', kwargs={'pk': 2})))

    #@todo add tests for the presence of the icon in the pages
