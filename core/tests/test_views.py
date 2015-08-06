from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model


User = get_user_model()


class AnyViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_cookie_notification_shown_variable_in_context_at_startup(self):
        response = self.client.get(reverse('home_page'))
        if response.context['cookies_notification_shown']:
            self.fail("The context variable cookies_notification_shown should be False at startup")

    def test_cookie_notification_shown_variable_in_context_after_acceptation(self):
        self.client.get(reverse('using_cookies_accepted'))
        response = self.client.get(reverse('home_page'))
        if not response.context['cookies_notification_shown']:
            self.fail("The context variable cookies_notification_shown should be True once accepted")
