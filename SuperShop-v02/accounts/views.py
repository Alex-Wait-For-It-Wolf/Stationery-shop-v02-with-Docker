from django.shortcuts import render
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
                                    PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.decorators import method_decorator

from loguru import logger

from .services import _deactivate_account_till_confirmed, \
                      _create_and_send_message_to_email, _get_user_by_uid, \
                      _activate_account_confirm_email, \
                      _get_user_by_email_from_the_form
from .forms import SignUpForm, ResendActivationEmailForm
from .tokens import account_activation_token

from common.decorators import block_authenticated_user


@method_decorator(logger.catch, name='post')
@method_decorator(logger.catch, name='get')
@method_decorator(block_authenticated_user, name='get')
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = _deactivate_account_till_confirmed(form)

            subject = 'Activate Your Account'
            message_template = 'accounts/account_activation_email.html'
            current_site = get_current_site(request)
            current_site_domain = current_site.domain
            _create_and_send_message_to_email(current_site_domain, user,
                                              subject, message_template)
            return render(request, 'accounts/account_activation_message.html')
        return render(request, self.template_name, {'form': form})


@method_decorator(logger.catch, name='get')
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        user = _get_user_by_uid(uidb64)
        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            _activate_account_confirm_email(user)
            login(request, user)
            return render(request, 'accounts/account_activation_success.html')
        else:
            return render(request, 'accounts/account_activation_error.html')


@method_decorator(logger.catch, name='post')
@method_decorator(logger.catch, name='get')
class ResendActivationEmailLink(View):
    form_class = ResendActivationEmailForm
    template_name = 'accounts/reactivate.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = _get_user_by_email_from_the_form(form)

            subject = 'Activate Your Account'
            message_template = 'accounts/account_activation_email.html'

            _create_and_send_message_to_email(request, user, subject,
                                              message_template)

            return render(request, 'accounts/account_activation_message.html')
        return render(request, self.template_name, {'form': form})

@method_decorator(logger.catch, name='dispatch')
class NewPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')

@method_decorator(logger.catch, name='dispatch')
class NewPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('accounts:password_reset_done')

@method_decorator(logger.catch, name='dispatch')
class NewPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
