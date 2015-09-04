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
        for prod in Product.objects.all():
            self._shop_page_contains('id="product_{}"'.format(prod.id), 1)

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
        self._shop_page_contains('<input name="quantity" value="{}"'.format(2), 1)

    def _test_set_cart_quantity_requires_saved_product(self):
        cat = insert_random_category()
        prod = Product(name="Product", price=100, category=cat)
        prod.set_cart_quantity(1)

    def test_set_cart_quantity_requires_saved_product(self):
        self.assertRaises(CantSetCartQuantityOnUnsavedProduct,
                          self._test_set_cart_quantity_requires_saved_product)

    def test_product_has_a_default_image(self):
        insert_random_product(random_image=False)
        self._shop_page_contains('src="/media/default/not_found.jpg"', 1)

    def test_product_default_image_is_loaded(self):
        response = self.client.get("/media/default/not_found.jpg")
        self.assertEqual(response.status_code, 200)

    def test_may_set_quantity_on_available_products(self):
        for i in range(0, 10):
            insert_random_product(stock=0)
        for i in range(0, 10):
            insert_random_product(stock=10)
        self._shop_page_contains('input name="quantity"', 10)


class SetProductQuantityAndGetCartTest(ViewsBaseTestCase):

    def test_cant_add_product_with_no_stock(self):
        insert_random_product(stock=0, price=100)
        response = self.client.get(reverse('set_product_quantity', kwargs=dict(product=1, quantity=1)))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {'error': "NO_STOCK"}
        )

    def test_cant_add_more_products_than_stock(self):
        insert_random_product(stock=1, price=100)
        response = self.client.get(reverse('set_product_quantity', kwargs=dict(product=1, quantity=2)))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {'error': "NOT_ENOUGH_STOCK", 'max': 1}
        )

    def test_added_product_to_cart_are_in_session(self, product_id=1, price=100, quantity=1):
        insert_random_product(stock=10, price=price)
        response = self.client.get(reverse('set_product_quantity',
                                           kwargs=dict(product=product_id, quantity=quantity)))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {"new_quantity": quantity}
        )

    def test_get_cart_with_empty_cart_returns_corresponding_json(self):
        response = self.client.get(reverse('get_cart'))

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [], 'total': 0, })

    def test_get_cart_returns_corresponding_json(self):
        self.test_added_product_to_cart_are_in_session()
        self.test_added_product_to_cart_are_in_session(product_id=2, price=1000, quantity=2)
        response = self.client.get(reverse('get_cart'))

        products = Product.objects.all()

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [
                {'id': 1, 'name': products[0].name, 'quantity': 1, 'price': 100},
                {'id': 2, 'name': products[1].name, 'quantity': 2, 'price': 2000}, ],
                'total': 2100, })

    def test_setting_quantity_to_zero_removes_entry_in_session(self):
        self.test_added_product_to_cart_are_in_session()
        self.client.get(reverse('set_product_quantity',
                                           kwargs=dict(product=1, quantity=0)))
        response = self.client.get(reverse('get_cart'))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [], 'total': 0, })
