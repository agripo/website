from core.tests.base import CoreTestCase
from core.forms import CheckoutForm
from django.utils import timezone


class CheckoutFormTest(CoreTestCase):

    def setUp(self):
        # We should have a user
        self.customer = self.create_user()
        # There should also be some delivery available
        self.deliveries = []
        for i in range(0, 5):
            date = timezone.now() + timezone.timedelta(i + 5)
            self.deliveries.append(
                self.create_delivery(delivery_point_name="Delivery point {}".format(i), date=date))

    def add_products_to_cart(self, number):
        category = self.create_category()
        for i in range(0, number):
            product = self.create_product(stock=10, name="Product {}".format(i), category=category)
            product.buy(5)

    def test_init(self):
        CheckoutForm(customer=self.customer)  # Should not raise

    def test_form_no_validation_for_blank_items(self):
        form = CheckoutForm(dict(delivery=None, message=""), customer=self.customer)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'delivery': ['This field is required.'],
        })

    def test_valid_data(self):
        self.add_products_to_cart(5)
        form = CheckoutForm({
            'delivery': self.deliveries[0].pk,
            'message': "Some message"
        }, customer=self.customer)
        self.assertTrue(form.is_valid())
        command = form.save()
        self.assertEqual(command.delivery, self.deliveries[0])
        self.assertEqual(command.message, "Some message")

    def test_blank_data(self):
        form = CheckoutForm({}, customer=self.customer)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'delivery': ['This field is required.'],
        })
