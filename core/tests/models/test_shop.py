from core.exceptions import AddedMoreToCartThanAvailable
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from core.tests.base import CoreTestCase
from core.models import ProductCategory, Product


class ProductCategoryModelTest(CoreTestCase):

    def test_category_should_have_a_name(self):
        cat = ProductCategory()
        self.assertRaises(ValidationError, cat.full_clean)

    def test_category_only_needs_a_name(self):
        cat = ProductCategory(name="Cat 1")
        cat.save()  # Should not raise


class ProductsModelTest(CoreTestCase):

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

    def _test_cant_add_more_than_available_to_cart(self):
        cat = self.create_category()
        prod = self.create_product(cat, stock=0)
        prod.set_cart_quantity(5)  # should raise an error

    def test_cant_add_more_than_available_to_cart(self):
        self.assertRaises(
            AddedMoreToCartThanAvailable, self._test_cant_add_more_than_available_to_cart)

    def test_product_quantity_defaults_to_zero(self):
        cat = self.create_category()
        prod = Product(pk=10, category=cat, name="Prod 1", price=10)
        prod.save()
        self.assertEqual(prod.get_cart_quantity(), 0)
