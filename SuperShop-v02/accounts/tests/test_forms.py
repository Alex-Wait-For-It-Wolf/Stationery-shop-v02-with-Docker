from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

import json

from ..forms import SignUpForm, ResendActivationEmailForm



class SignUpTests(TestCase):
    username = 'newuser'
    first_name = 'John'
    last_name = 'Doe'
    email = 'newuser@email.com'
    password = 'testpassword'
    password_1 = 'testpassword1'


    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_form_is_instance_of_same_class(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_signup_form_contain_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_form_with_valid_data_without_optional_fields(self):
        form_data = {'username': self.username,'email': self.email,
                     'password1': self.password_1, 'password2': self.password_1}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_with_valid_data_with_optional_fields(self):
        form_data = {'username': self.username, 'first_name': self.first_name,
                     'last_name': self.last_name, 'email': self.email,
                     'password1': self.password_1, 'password2': self.password_1}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_can_not_create_with_same_email(self):
        old_user = get_user_model().objects.create_user(self.username,
                                                        self.email,
                                                        self.password,)
        form_data = {'username': 'newuser01', 'email': self.email,
                     'password1': 'newpass01234', 'password2': 'newpass01234'}
        form = SignUpForm(data=form_data)
        form_error = json.loads(form.errors.as_json())
        self.assertFalse(form.is_valid())

        error_message = 'This email address is already in use.'
        form_exception = _return_dictionary_with_exception_from_form(form)
        self.assertEqual(form_exception['message'],error_message)


class ResendActivationEmailFormTest(TestCase):
    username = 'newuser01'
    email = 'newuser01@gmail.com'
    password = 'testpassword'


    def setUp(self):
        url = reverse('accounts:resend_email_link')
        self.response = self.client.get(url)

    def test_resend_form_is_instance_of_same_class(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ResendActivationEmailForm)

    def test_resend_form_contain_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_with_valid_data(self):
        existing_user = get_user_model().objects.create_user(self.username,
                                                             self.email,
                                                             self.password,)
        existing_user.is_active = False
        existing_user.save()
        form_data = {'email': self.email}
        form = ResendActivationEmailForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_no_account_with_this_email(self):
        form_data = {'email': self.email}
        form = ResendActivationEmailForm(data=form_data)
        self.assertFalse(form.is_valid())

        error_message = "There's no account with the email that you provided."
        form_exception = _return_dictionary_with_exception_from_form(form)
        self.assertEqual(form_exception['message'], error_message)

    def test_account_is_already_active(self):
        existing_user = get_user_model().objects.create_user(self.username,
                                                             self.email,
                                                             self.password,)
        form_data = {'email': 'newuser01@gmail.com'}
        form = ResendActivationEmailForm(data=form_data)
        self.assertFalse(form.is_valid())

        error_message = "This account is active"
        form_exception = _return_dictionary_with_exception_from_form(form)
        self.assertEqual(form_exception['message'],error_message)

def _return_dictionary_with_exception_from_form(form):
    """
    Compare exceptin message from the from, and any message,
    that you provide.
    """
    form_error_in_dictionary = json.loads(form.errors.as_json())
    list_with_error = form_error_in_dictionary['email']
    dictionary_with_error_from_list = list_with_error[0]
    return dictionary_with_error_from_list
