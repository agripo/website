from core.exceptions import AddedMoreToCartThanAvailable
from django.db import IntegrityError

from core.tests.base import CoreTestCase
from core.models import Stock


class StockModelTest(CoreTestCase):

    def _create_stock(self, product=None, user=None, stock=0, save=True):
        if not user:
            user = self.create_user().add_to_farmers()

        if not product:
            cat = self.create_category()
            product = self.create_product(cat)

        the_stock = Stock(product=product, farmer=user)
        if save:
            the_stock.save()
            the_stock.set(stock)  # This calls save() in the background
        elif stock > 0:
            raise Exception("Can't use _create_stock() with stock>0 and save=False together")

        return the_stock

    def test_cant_update_simple_users_stock(self):
        user = self.create_user()
        stock = self._create_stock(user=user, save=False)
        self.assertRaises(IntegrityError, stock.save)

    def test_one_farmer_cant_have_multiple_stocks_for_one_product(self):
        user = self.create_user().add_to_farmers()
        cat = self.create_category()
        prod = self.create_product(cat)
        self._create_stock(prod, user, 0)
        stock2 = self._create_stock(prod, user, 0, save=False)
        self.assertRaises(IntegrityError, stock2.save)

    def test_stock_gets_updated_using_set(self):
        stock = self._create_stock()
        stock.set(50)
        self.assertEqual(stock.stock, 50)

    def test_product_stock_updates_when_stock_changes(self):
        stock = self._create_stock(stock=10)
        prod = stock.product
        self.assertEqual(prod.stock, 10)
        stock.set(5)
        self.assertEqual(prod.stock, 5)
        user = self.create_user("Jean-Pierre").add_to_farmers()
        self._create_stock(product=prod, user=user, stock=10)
        self.assertEqual(prod.stock, 15)

    def test_empty_stock_is_not_available(self):
        stock = self._create_stock(stock=0)
        self.assertFalse(stock.product.is_available())

    def test_product_with_stock_is_available(self):
        stock = self._create_stock(stock=5)
        self.assertTrue(stock.product.is_available())

    def test_available_stock(self):
        stock = self._create_stock(stock=5)
        self.assertEqual(stock.product.available_stock(), 5)

    def test_exception_when_adding_more_than_available_to_cart(self):
        stock = self._create_stock(stock=5)
        try :
            stock.product.set_cart_quantity(6)
            raise Exception("AddedMoreToCartThanAvailable should have been raised")
        except AddedMoreToCartThanAvailable:
            pass
