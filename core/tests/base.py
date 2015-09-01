from django.test import TestCase


class CoreTestCase(TestCase):

    def not_implemented(self):
        self.fail("Test not implemented yet")
