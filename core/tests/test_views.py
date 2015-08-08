from django.test import TestCase

from core.authentication import force_production_server
from core.models import AgripoUser as User


class LoginViewTest(TestCase):

    def tearDown(self):
        force_production_server(False)

    def auto_connect(self, email):
        return self.client.get('/core/auto_login/{}'.format(email))

    def test_can_auto_connect_with_new_email(self):
        page = self.auto_connect('alpha@test.com')
        self.assertEqual(page.content.decode(page.charset), "{} is connected".format('alpha@test.com'))
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
