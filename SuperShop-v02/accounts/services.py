from django.shortcuts import render
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from loguru import logger

from .tokens import account_activation_token


@logger.catch
def _deactivate_account_till_confirmed(form):
    """Deactivate account till user confirm his email."""
    user = form.save(commit=False)
    user.is_active = False # Deactivate account till it is confirmed
    user.save()
    return user

@logger.catch
def _create_and_send_message_to_email(current_site_domain, user,
                                      subject, message_template):
    """
    Create and send message with appropriate subject
    to current user email.
    """
    message = render_to_string(message_template, {
        'user': user,
        'domain': current_site_domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)

@logger.catch
def _get_user_by_uid(uidb64):
    """
    Try get user by uid, return user if everything is ok,
    or None if error occurs.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    else:
        return user

@logger.catch
def _activate_account_confirm_email(user):
    """
    Activate user account,
    confirm email.
    """
    user.is_active = True
    user.profile.email_confirmed = True
    user.profile.save()
    user.save()

@logger.catch
def _get_user_by_email_from_the_form(form):
    """Get and return user by email from the form."""
    email = form.cleaned_data.get('email')
    user = User.objects.get(email=email)
    return user
