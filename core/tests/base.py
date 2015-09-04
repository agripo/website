from django.test import TestCase

from core.models import ProductCategory, AgripoUser as User, Product
from core.models import SiteConfiguration


class CoreTestCase(TestCase):

    def setUp(self):
        self.config = SiteConfiguration.objects.get()

    def not_implemented(self):
        self.fail("Test not implemented yet")

    def create_category(self):
        cat = ProductCategory(name="Cat 1")
        cat.save()
        return cat

    def create_product(self, category, stock=0):
        prod = Product(name="Product", category=category, price=100, stock=stock)
        prod.save()
        return prod

    def create_user(self, username="Jean-Claude"):
        user = User(username=username, password="my_pass", email="mail@dom.net")
        user.save()
        return user
