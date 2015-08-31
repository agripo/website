from .core import CoreTestCase
from core.authentication import force_production_server
from core.models import AgripoUser as User, SiteConfiguration


config = SiteConfiguration.objects.get()
NUMBER_OF_NEWS_BY_PAGE = config.news_count


class LoginViewTest(CoreTestCase):

    def test_can_auto_connect_with_new_email(self):
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "{} is connected as user".format('alpha@test.com'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_can_auto_connect_as_manager_with_new_email(self):
        page = self.auto_manager_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "{} is connected as manager".format('alpha@test.com'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_cant_auto_connect_with_existing_email(self):
        User.objects.create(email="alpha@test.com")
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "No autoconnection with existing user")
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_cant_auto_connect_on_production_server(self):
        force_production_server(True)  # deactivation is made in TearDown
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "No autoconnection on production server")
        self.assertNotIn('_auth_user_id', self.client.session)
