from core.forms import CheckoutForm
from django.test import TestCase

from core.models import ProductCategory, AgripoUser as User, Product, DeliveryPoint, Delivery, Command
from core.models import SiteConfiguration
from django.utils import timezone


class CoreTestCase(TestCase):

    def setUp(self):
        self.config = SiteConfiguration.objects.get()

    def not_implemented(self):
        self.fail("Test not implemented yet")

    def create_delivery_point(self, name="One delivery point"):
        dp = DeliveryPoint(name=name, description="Some description for delivery point {}".format(name))
        dp.save()
        return dp

    def create_delivery(self, delivery_point=None, delivery_point_name="One delivery point"):
        if not delivery_point:
            delivery_point = self.create_delivery_point(name=delivery_point_name)

        delivery = Delivery(date=timezone.now(), delivery_point=delivery_point)
        delivery.save()
        return delivery

    def create_command(self, user=None, delivery=None, delivery_point_name="One delivery point"):
        if not user:
            user = self.create_user()

        if not delivery:
            delivery = self.create_delivery(delivery_point_name=delivery_point_name)

        if not Product.static_get_cart_products():
            product = self.create_product(stock=5)
            product.save()
            product.set_cart_quantity(2)

        command = Command(delivery=delivery, customer=user)
        command.save()
        return command

    def create_category(self):
        cat = ProductCategory(name="Cat 1")
        cat.save()
        return cat

    def create_product(self, category=None, stock=0, name="Product"):
        if not category:
            category = self.create_category()

        prod = Product(name=name, category=category, price=100, stock=stock)
        prod.save()
        return prod

    def create_user(self, username="Jean-Claude"):
        user = User(username=username, password="my_pass", email="mail@dom.net")
        user.save()
        return user
