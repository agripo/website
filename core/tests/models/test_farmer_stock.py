from core.tests.base import CoreTestCase
from core.models import Product, Farmer


class FarmerModelTest(CoreTestCase):

    def test_farmer_must_have_email(self):
        self.not_implemented()

    def test_farmer_has_phone(self):
        self.not_implemented()

    def test_farmer_stock_update_updates_last_stock_update_field(self):
        self.not_implemented()


class StockModelTest(CoreTestCase):
    '''
    The model here is used in a through relationship
    '''
    def test_stocks_are_updated_when_one_farmer_declares_hes_stock(self):
        self.not_implemented()

    def test_(self):
        self.not_implemented()
