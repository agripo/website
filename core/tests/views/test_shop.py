from core.exceptions import CantSetCartQuantityOnUnsavedProduct, AddedMoreToCartThanAvailable
from django.core.urlresolvers import reverse

from core.tests.views.base import ViewsBaseTestCase
from core.models import Product
from core.management.commands.populatedb import (
    insert_random_categories_and_products, insert_random_category, insert_random_product)


class ShopViewTest(ViewsBaseTestCase):

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
        insert_random_categories_and_products(5, 4)
        self._shop_page_contains('Produit indisponible pour le moment', 20)

    def _test_limit_cart_quantity_to_stock(self):
        prod = insert_random_product(stock=2)
        prod.set_cart_quantity(5)

    def test_limit_cart_quantity_to_stock(self):
        self.assertRaises(AddedMoreToCartThanAvailable, self._test_limit_cart_quantity_to_stock)

    def test_display_all_categories(self):
        insert_random_categories_and_products(5, 0)
        self._shop_page_contains('class="one_product_category"', 5)

    def test_display_message_for_empty_categories(self):
        insert_random_categories_and_products(2, 1)
        insert_random_categories_and_products(2, 0)
        self._shop_page_contains('class="one_product_category_empty"', 2)

    def test_prefill_quantity_from_cart(self):
        prod = insert_random_product(stock=3)
        prod.set_cart_quantity(2)
        self._shop_page_contains('<span>{} unités</span>'.format(2), 1)

    def _test_set_cart_quantity_requires_saved_product(self):
        cat = insert_random_category()
        prod = Product(name="Product", price=100, category=cat)
        prod.set_cart_quantity(1)

    def test_set_cart_quantity_requires_saved_product(self):
        self.assertRaises(CantSetCartQuantityOnUnsavedProduct,
                          self._test_set_cart_quantity_requires_saved_product)

    def test_product_has_a_default_image(self):
        insert_random_categories_and_products(2, 2)
        self._shop_page_contains('src="/media/default/not_found.jpg"', 4)

    def test_product_default_image_is_loaded(self):
        response = self.client.get("/media/default/not_found.jpg")
        self.assertEqual(response.status_code, 200)

    def test_may_set_quantity_on_available_products(self):
        for i in range(0, 10):
            insert_random_product(stock=0)
        for i in range(0, 10):
            insert_random_product(stock=10)
        self._shop_page_contains('input name="quantity"', 10)
