from django.contrib.auth.views import LoginView, LogoutView
from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpRequest


from ..views import SignUpView
from common.decorators import block_authenticated_user

class SignUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_url_resolves_signupview(self):
        view = resolve('/en/accounts/signup/')
        self.assertEqual(view.func.__name__,
                         SignUpView.as_view().__name__)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/signup.html')
        self.assertContains(self.response, 'Create new account')
        self.assertNotContains(self.response,
                               'Hi there! I should not be on the page.')

    def test_signup_page_resolve_url(self):
        resolver = resolve('/en/accounts/signup/')
        self.assertEqual(resolver.view_name, 'accounts:signup')

    def test_signup_page_reverse_url(self):
        url = reverse('accounts:signup')
        self.assertEqual(url, '/en/accounts/signup/')


class LogInTests(TestCase):

    def setUp(self):
        url = reverse('accounts:login')
        self.response = self.client.get(url)

    def test_login_url_resolves_loginview(self):
        view = resolve('/en/accounts/login/')
        self.assertEqual(view.func.__name__,
                         block_authenticated_user(LoginView.as_view()).__name__)

    def test_login_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Log-in')
        self.assertNotContains(self.response,
                               'Hi there! I should not be on the page.')

    def test_login_page_resolve_url(self):
        resolver = resolve('/en/accounts/login/')
        self.assertEqual(resolver.view_name, 'accounts:login')

    def test_login_page_reverse_url(self):
        url = reverse('accounts:login')
        self.assertEqual(url, '/en/accounts/login/')
