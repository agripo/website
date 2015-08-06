from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model, SESSION_KEY

from accounts.authentication import force_production_server

User = get_user_model()


class LoginViewTest(TestCase):

    def tearDown(self):
        force_production_server(False)

    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this')

    @patch('accounts.views.authenticate')
    def test_returns_OK_when_user_found(self, mock_authenticate):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(response.content.decode(), 'OK')

    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(self, mock_authenticate):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertNotIn(SESSION_KEY, self.client.session) 

    def auto_connect(self, email):
        return self.client.get('/accounts/auto_login/{}'.format(email))

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
