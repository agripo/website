from django.core.urlresolvers import reverse

from .core import CoreTestCase
from core.models import SiteConfiguration, Product
from core.management.commands.populatedb import (
    insert_random_categories_and_products)


config = SiteConfiguration.objects.get()
NUMBER_OF_NEWS_BY_PAGE = config.news_count


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

    def test_limit_cart_quantity_to_stock(self):
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
