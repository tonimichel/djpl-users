from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.views import (
    password_reset_confirm,
    password_reset,
    password_reset_done,
    password_reset_complete,
    login,
    LogoutView,
)
from django.urls import re_path, path
from django.views.generic import TemplateView
from users.forms import AuthenticationForm

from .forms import get_password_reset_form
from . import forms as users_forms
from .views import password_reset_confirm as account_confirm


def get_patterns(user_model):
    # Registration urls
    return [
        path(
            settings.LOGIN_URL.lstrip('/'),
            login,
            dict(
                template_name='users/login.html',
                authentication_form=AuthenticationForm,
                extra_context=dict(
                    password_reset_url='/users/password_reset/',
                    login_url=settings.LOGIN_URL,
                    next=settings.LOGIN_REDIRECT_URL,
                    login_view=True
                )
            ),
            name='users-login'
        ),
        path(
            'users/logout/',
            LogoutView.as_view(**dict(
                template_name='users/logged_out.html',
                next_page=settings.LOGOUT_REDIRECT_URL
            )),
            name='users-logout'
        ),
        # account confirmation url, protected by secret token; displayed when the users clicked the account confirm url
        # in its account confirmation email
        re_path(
            r'^users/account_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            account_confirm, dict(
                template_name='users/account_confirm.html',
                set_password_form=users_forms.AccountActivationPasswordForm,
                post_reset_redirect='/users/account_confirm_complete/',
                user_model=user_model
            ),
            name='users-account_confirm'
        ),
        # indicated that the account was successfully confirmed
        path(
            'users/account_confirm_complete/',
            TemplateView.as_view(
                template_name='users/account_confirm_complete.html',
                extra_context=dict(
                    login_redirect_url=settings.LOGIN_REDIRECT_URL,
                    login_url=settings.LOGIN_URL,
                    user_model=user_model
                )
            ),
            name='users-account_confirm_complete'
        ),

        # displays a form that takes a user's email address; when submitted, an email with a password reset url is sent
        # to that user
        path(
            'users/password_reset/',
            password_reset, dict(
                template_name='users/password_reset.html',
                post_reset_redirect='/users/password_reset_done/',
                email_template_name='users/email/password_reset.html',
                password_reset_form=get_password_reset_form('users-password_reset_confirm', user_model),
            ),
            name='users-password_reset'
        ),
        # displays that the password change email has been sent.
        path(
            'users/password_reset_done/',
            password_reset_done, dict(
                template_name='users/password_reset_done.html',
                extra_context=dict(login_url=settings.LOGIN_URL),
            ),
            name='users-password-reset-done'
        ),
        # displays the form where the user can choose its new password
        re_path(
            r'^users/password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            password_reset_confirm, dict(
                template_name='users/password_reset_confirm.html',
                post_reset_redirect='/users/password_reset_complete/',
            ),
            name='users-password_reset_confirm'
        ),
        # indicates that the user's password has been successfully changed.
        path(
            'users/password_reset_complete/',
            password_reset_complete, dict(
                template_name='users/password_reset_complete.html',
                extra_context=dict(login_url=settings.LOGIN_URL)
            ),
            name='user-password_reset_complete'
        )
    ]
