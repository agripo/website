from core.exceptions import CantSetCartQuantityOnUnsavedProduct, AddedMoreToCartThanAvailable
from django.core.urlresolvers import reverse

from core.tests.views.base import ViewsBaseTestCase
from core.models.shop import Product, Delivery
from core.management.commands.populatedb import (
    insert_random_categories_and_products, insert_random_category, insert_random_product)
from django.utils import timezone


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
        user = self.create_user()
        prod = insert_random_product(stock=2)
        prod.set_cart_quantity(user, 5)

    def test_limit_cart_quantity_to_stock(self):
        self.assertRaises(AddedMoreToCartThanAvailable, self._test_limit_cart_quantity_to_stock)

    def test_display_all_categories(self):
        insert_random_categories_and_products(5, 0)
        self._shop_page_contains('class="one_product_category"', 5)

    def test_display_message_for_empty_categories(self):
        insert_random_categories_and_products(2, 1)
        insert_random_categories_and_products(2, 0)
        self._shop_page_contains('class="one_product_category_empty"', 2)

    def _test_set_cart_quantity_requires_saved_product(self):
        user = self.create_user()
        cat = insert_random_category()
        prod = Product(name="Product", price=100, category=cat)
        prod.set_cart_quantity(user, 1)

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


class ShopCheckoutTest(ViewsBaseTestCase):

    def setUp(self):
        super().setUp()
        self.auto_connect("test@gmail.com")

    def test_cant_display_checkout_page_without_products_in_the_cart(self):
        response = self.client.get(reverse('checkout'))
        self.assertRedirects(response, reverse("shop_page"), 302)

    def test_checkout_form_uses_right_template(self):
        insert_random_product(stock=1, price=100)
        self.client.get(reverse('set_product_quantity', kwargs=dict(product=1, quantity=1)))
        response = self.client.get(reverse('checkout'))
        self.assertTemplateUsed(response, 'core/checkout.html')

    def _add_products_to_cart(self, number):
        rep = dict(total=0, products=[])
        for i in range(1, number + 1):
            insert_random_product(stock=i, price=i * 100)
            self.client.get(reverse('set_product_quantity', kwargs=dict(product=i, quantity=i)))
            rep['total'] += i * i * 100
            rep['products'].append(dict(quantity=i, product=Product.objects.get(pk=i)))

        return rep

    def test_display_right_products(self):
        cart = self._add_products_to_cart(3)
        response = self.client.get(reverse('checkout'))
        for prod in cart['products']:
            self.assertContains(response, 'id="bought_product_{}"'.format(prod['product'].id))

    def test_display_products_unit_prices(self):
        cart = self._add_products_to_cart(3)
        response = self.client.get(reverse('checkout'))
        for prod in cart['products']:
            self.assertContains(response, '{} FCFA'.format(prod['product'].price))

    def test_display_products_quantity_prices(self):
        cart = self._add_products_to_cart(3)
        response = self.client.get(reverse('checkout'))
        for prod in cart['products']:
            self.assertContains(response, '{} FCFA'.format(prod['product'].price * prod['quantity']))

    def test_display_right_total_price(self):
        cart = self._add_products_to_cart(3)
        response = self.client.get(reverse('checkout'))
        self.assertContains(response, '{} FCFA'.format(cart['total']))

    def test_cant_select_already_done_deliveries_for_checkout(self):
        Delivery.objects.all().update(done=True)
        self._add_products_to_cart(3)
        response = self.client.get(reverse('checkout'))
        queryset = response.context_data['form'].fields['delivery'].choices.queryset
        self.assertEqual(queryset.count(), 0)

    def test_ten_next_available_deliveries_are_available_for_checkout(self):
        Delivery.objects.all().update(done=True)
        self._add_products_to_cart(3)
        deliveries = []
        for i in range(0, 15):
            # 2 in the past, 13 in the future
            deliveries.append(self.create_delivery(
                date=timezone.now() + timezone.timedelta(seconds=i - 1), delivery_point_name="DP {}".format(i)))

        response = self.client.get(reverse('checkout'))
        queryset = response.context_data['form'].fields['delivery'].choices.queryset
        self.assertEqual(queryset.count(), 10)
        for delivery in deliveries[2:12]:
            looking_for = '<option value="{}">{}</option>'.format(delivery.pk, delivery.__str__())
            self.assertContains(response, looking_for, html=True)


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

    def test_added_product_to_cart_are_in_stored(self, product_id=1, price=100, quantity=1):
        insert_random_product(stock=10, price=price)
        self.auto_connect("test@gmail.com")
        response = self.client.get(reverse('set_product_quantity',
                                           kwargs=dict(product=product_id, quantity=quantity)))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), {"new_quantity": quantity}
        )

    def test_get_cart_with_empty_cart_returns_corresponding_json(self):
        self.auto_connect("test@gmail.com")
        response = self.client.get(reverse('get_cart'))

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [], 'total': 0, })

    def test_get_cart_returns_corresponding_json(self):
        self.test_added_product_to_cart_are_in_stored()
        self.test_added_product_to_cart_are_in_stored(product_id=2, price=1000, quantity=2)
        response = self.client.get(reverse('get_cart'))

        products = Product.objects.all()

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [
                {'id': 1, 'name': products[0].name, 'quantity': 1, 'price': 100},
                {'id': 2, 'name': products[1].name, 'quantity': 2, 'price': 2000}, ],
                'total': 2100, })

    def test_setting_quantity_to_zero_removes_entry_in_session(self):
        self.test_added_product_to_cart_are_in_stored()
        self.client.get(reverse('set_product_quantity',
                                           kwargs=dict(product=1, quantity=0)))
        response = self.client.get(reverse('get_cart'))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'products': [], 'total': 0, })


class DeliveryDetailsViewTest(ViewsBaseTestCase):

    def test_uses_right_template(self):
        self.not_implemented()

    def test_shows_total(self):
        self.not_implemented()

    def test_shows_consolidated_products_list(self):
        self.not_implemented()

    def test_displays_all_commands(self):
        self.not_implemented()

    def test_shows_users_data(self):
        self.not_implemented()

    def test_displays_command_products_data(self):
        self.not_implemented()

    def test_displays_command_total(self):
        self.not_implemented()

    def test_displays_instructions(self):
        self.not_implemented()

    def test_displays_message_if_no_command(self):
        self.not_implemented()
