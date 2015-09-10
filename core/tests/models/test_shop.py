from core.exceptions import AddedMoreToCartThanAvailable
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from core.tests.base import CoreTestCase
from core.models.shop import ProductCategory, Product, DeliveryPoint, Delivery, Command, CommandProduct


class ShopCoreTestCase(CoreTestCase):
    pass


class DeliveryModelTest(ShopCoreTestCase):

    def test_has_an_explicit__str__(self):
        dp = self.create_delivery_point(name="Point")
        self.assertNotEquals(dp.__str__(), 'DeliveryPoint object')

    def test_must_have_a_deliverypoint(self):
        d = Delivery()
        self.assertRaises(IntegrityError, d.save)

    def test_bought_products_are_listed(self):
        self.not_implemented()

    def test_same_product_from_multiple_commands_are_added(self):
        self.not_implemented()

    def test_total_price_calculated_correctly(self):
        self.not_implemented()


class DeliveryPointModelTest(ShopCoreTestCase):

    def test_has_an_explicit__str__(self):
        dp = self.create_delivery_point(name="Point")
        d = Delivery(date=timezone.now(), delivery_point=dp)
        self.assertNotEquals(d.__str__(), 'Delivery object')

    def test_fullname_is_unique(self):
        dp = DeliveryPoint(name="One name")
        dp.save()
        dp2 = DeliveryPoint(name="One name")
        self.assertRaises(IntegrityError, dp2.save)


class CommandProductModelTest(ShopCoreTestCase):

    def test_quantity_cant_be_0(self):
        product = self.create_product(stock=5)
        product.set_cart_quantity(2)
        command = self.create_command()
        cp = CommandProduct(command=command, product=product, quantity=0)
        with self.assertRaises(ValidationError):
            cp.full_clean()


class CommandModelTest(ShopCoreTestCase):

    def test_user_may_have_multiple_commands_for_different_deliveries(self):
        user = self.create_user()
        delivery = self.create_delivery(delivery_point_name="Point 1")
        delivery2 = self.create_delivery(delivery_point_name="Point 2")
        self.create_command(user=user, delivery=delivery)
        self.create_command(user=user, delivery=delivery2)  # Should not raise

    def test_user_may_have_multiple_commands_for_same_delivery(self):
        user = self.create_user()
        delivery = self.create_delivery()
        self.create_command(user=user, delivery=delivery)
        self.create_command(user=user, delivery=delivery)  # Should not raise

    def test_command_must_have_a_user_set(self):
        delivery = self.create_delivery()
        command = Command(delivery=delivery)
        with self.assertRaises(ValidationError):
            command.full_clean()

    def _validate_command(self, product=None, available_quantity=10, bought_quantity=5):
        if not product:
            product = self.create_product(stock=available_quantity)

        product.set_cart_quantity(bought_quantity)  # should not raise
        command = self.create_command()
        command.validate()
        return command

    def test_validating_command_empties_session_cart(self):
        self._validate_command()
        self.assertEqual(Product.static_get_cart_products(), [])

    def test_validating_command_links_to_products(self):
        command = self._validate_command()
        product = Product.objects.get(id=1)
        self.assertEqual(command.products.all()[0], product)

    def test_validating_command_removed_products_from_stocks(self):
        product = self.create_product(stock=10)
        init_stock = product.available_stock()
        self._validate_command(product=product, bought_quantity=5)
        product = Product.objects.get(id=1)
        self.assertEqual(product.available_stock(), init_stock - 5)

    def test_cant_validate_command_when_stock_isnt_enough(self):
        product = self.create_product(stock=10)
        product.set_cart_quantity(10)
        command = self.create_command()
        product.stock = 8
        product.save()

        self.assertRaises(AddedMoreToCartThanAvailable, command.validate)

    def test_validated_command_written_as_not_sent(self):
        command = self._validate_command()
        self.assertEquals(command.is_sent(), False)

    def test_sent_command_written_as_so(self):
        command = self._validate_command().send()
        self.assertEquals(command.is_sent(), True)

    def test_send_supports_method_chaining(self):
        command = self._validate_command()
        command2 = command.send()
        self.assertEquals(command, command2)

class ProductCategoryModelTest(ShopCoreTestCase):

    def test_category_should_have_a_name(self):
        cat = ProductCategory()
        self.assertRaises(ValidationError, cat.full_clean)

    def test_category_only_needs_a_name(self):
        cat = ProductCategory(name="Cat 1")
        cat.save()  # Should not raise


class ProductsModelTest(ShopCoreTestCase):

    def test_cant_buy_more_than_stock(self):
        product = self.create_product(stock=10)
        with self.assertRaises(AddedMoreToCartThanAvailable):
            product.buy(15)

    def test_buy_updates_available_stock(self):
        product = self.create_product(stock=10)
        product.buy(5)
        self.assertEquals(product.available_stock(), 5)

    def test_available_stock_is_stock_when_nothing_is_bought(self):
        product = self.create_product(stock=10)
        self.assertEquals(product.available_stock(), 10)

    def test_set_cart_quantity_allows_method_chaining(self):
        product = self.create_product(stock=10)
        product2 = product.set_cart_quantity(10)
        self.assertEqual(product, product2)

    def test_buy_allows_method_chaining(self):
        product = self.create_product(stock=10)
        product2 = product.buy(5)
        self.assertEqual(product, product2)

    def test_product_should_have_a_name(self):
        cat = self.create_category()
        prod = Product(category=cat, price=100)
        self.assertRaises(ValidationError, prod.full_clean)

    def test_product_should_have_a_category(self):
        prod = Product(name="Prod 1", price=100)
        self.assertRaises(IntegrityError, prod.save)

    def test_product_price_cant_be_zero(self):
        cat = self.create_category()
        prod = Product(category=cat, name="Prod 1", price=0)
        self.assertRaises(ValidationError, prod.full_clean)

    def test_product_cant_be_negative(self):
        cat = self.create_category()
        prod = Product(category=cat, name="Prod 1", price=-10)
        self.assertRaises(ValidationError, prod.full_clean)

    def test_can_set_cart_quantity(self):
        cat = self.create_category()
        prod = self.create_product(cat, stock=10)
        prod.set_cart_quantity(5)  # should not raise
        self.assertEqual(prod.get_cart_quantity(), 5)

    def test_set_cart_quantity_updates_session(self):
        cat = self.create_category()
        prod = self.create_product(cat, stock=10)
        prod.set_cart_quantity(5)  # should not raise
        prod = Product.objects.get(name="Product")  # reloads the object from the db
        self.assertEqual(prod.get_cart_quantity(), 5)

    def test_cant_add_more_than_available_to_cart(self):
        cat = self.create_category()
        prod = self.create_product(cat, stock=0)
        with self.assertRaises(AddedMoreToCartThanAvailable):
            prod.set_cart_quantity(5)

    def test_product_quantity_defaults_to_zero(self):
        cat = self.create_category()
        prod = Product(pk=10, category=cat, name="Prod 1", price=10)
        prod.save()
        self.assertEqual(prod.get_cart_quantity(), 0)
