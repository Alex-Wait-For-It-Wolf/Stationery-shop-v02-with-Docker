import json
from django.test import TestCase
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from ..forms import SignUpForm, ResendActivationEmailForm
from ..services import (_deactivate_account_till_confirmed,
                        _create_and_send_message_to_email as create_send,
                        _get_user_by_uid, _activate_account_confirm_email,
                        _get_user_by_email_from_the_form)
from ..tokens import account_activation_token


class AccountServicesTests(TestCase):

    def setUp(self):
        self.username = 'testusername95'
        self.email = 'testemail025@gmai.com'
        self.password = 'testpass8535'

        self.form_data = {'username': self.username, 'email': self.email,
                        'password1': self.password, 'password2': self.password}

        self.form = SignUpForm(data=self.form_data)
        self.user = _deactivate_account_till_confirmed(self.form)

        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.user_by_uid = _get_user_by_uid(uidb64)

    def test_deactivate_account(self):
        self.assertTrue(self.form.is_valid())
        self.assertFalse(self.user.is_active)

    def test_create_and_send_message_to_email(self):
        current_site_domain = 'hellothisistest.com'
        subject = 'Activate Your Account'
        message_template = 'accounts/account_activation_email.html'
        message_to_email = create_send(current_site_domain,
                                       self.user, subject,
                                       message_template)

        message = render_to_string(message_template, {
            'user': self.user,
            'domain': current_site_domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user),
        })
        self.assertEqual(message_to_email, self.user.email_user(subject,
                                                                message))

    def test_get_user_by_uid(self):
        self.assertEqual(self.user_by_uid.username, self.username)

        id_of_none = urlsafe_base64_encode(force_bytes(5))
        value_for_error = urlsafe_base64_encode(force_bytes('dawk'))

        user_does_not_exist = _get_user_by_uid(id_of_none)
        value_error = _get_user_by_uid(value_for_error)

        self.assertEqual(user_does_not_exist, None)
        self.assertEqual(value_error, None)

    def test_activate_account_confirm_email(self):
        user = self.user_by_uid
        self.assertFalse(user.is_active)
        self.assertFalse(user.profile.email_confirmed)

        activate_account = _activate_account_confirm_email(user)

        self.assertTrue(user.is_active)
        self.assertTrue(user.profile.email_confirmed)

    def test_get_user_by_email_from_the_form(self):
        form_data = {'email': self.email}
        form = ResendActivationEmailForm(data=form_data)
        valid_form = form.is_valid()
        user = _get_user_by_email_from_the_form(form)
        self.assertEquals(user.username, self.username)
