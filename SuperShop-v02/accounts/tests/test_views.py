from django.test import RequestFactory, TestCase
from django.urls import reverse, resolve
from django.contrib.auth.views import LoginView, LogoutView

from ..views import SignUpView, ActivateAccount, ResendActivationEmailLink
from ..forms import SignUpForm
from common.decorators import block_authenticated_user


class SignUpTests(TestCase):

    def test_signup_url_resolves_singup_view(self):
        view = resolve('/en/accounts/signup/')
        self.assertEqual(view.func.__name__, SignUpView.as_view().__name__)

    def test_get_signup_view(self):
        response = self.client.get('/en/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_post_signup_view(self):
        response = self.client.post('/en/accounts/signup/',
                                                    {'username': 'jordy',
                                                    'email': 'dhajw@gmail.com',
                                                    'password1': 'dajsdhkaw',
                                                    'password2': 'dajsdhkaw'})
        self.assertEqual(response.status_code, 200)


class ActivateAccountTests(TestCase):

    def test_activate_account_view(self):
        view = resolve('/en/accounts/activate/MjU/5nu-7beb1b2d30e79367b363/')
        self.assertEqual(view.func.__name__,
                         ActivateAccount.as_view().__name__)

    def test_get_signup_view(self):
        response = self.client.get('/en/accounts/activate/MjU/5nu-7beb1b2d30e79367b363/')
        self.assertEqual(response.status_code, 200)


class ReactivateAccountTests(TestCase):

    def test_reactivate_account_view(self):
        view = resolve('/en/accounts/reactivate/')
        self.assertEqual(view.func.__name__,
                         ResendActivationEmailLink.as_view().__name__)


class LogInTests(TestCase):

    def test_login_view_name(self):
        view = resolve('/en/accounts/login/')
        self.assertEqual(view.func.__name__,
                         block_authenticated_user(LoginView.as_view()).__name__)


class LogOutTests(TestCase):

    def test_logout_view_name(self):
        view = resolve('/en/accounts/logout/')
        self.assertEqual(view.func.__name__,
                         LogoutView.as_view().__name__)
