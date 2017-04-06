# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib.auth.views import password_change, password_change_done, password_reset_confirm, password_reset, password_reset_done, password_reset_complete, login, logout
from .views import password_reset_confirm as account_confirm
from users.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.conf import settings
from .forms import get_password_reset_form


def _logout(request, **kws):
    return logout(request, **kws)


def get_patterns(user_model):

    conf = user_model.appconfig
    URLNAMES = user_model.urlnames

    # ensure ending slashes if URL_PREFIX is provided
    if len(conf.URL_PREFIX) > 0 and not conf.URL_PREFIX.endswith('/'):
        conf.URL_PREFIX += '/'

    login_url = settings.LOGIN_URL
    if not login_url.startswith('/'):
        login_url = '/' + login_url

    login_url_for_pattern = ''.join(login_url[1:])

    login_redirect_url = settings.LOGIN_REDIRECT_URL
    logout_view_args = dict(template_name='users/logged_out.html')
    logout_view_args['next_page'] = settings.LOGOUT_REDIRECT_URL

    # Registration urls
    return [
        url(
            r'^%s$' % login_url_for_pattern,
            login, {
                'template_name': 'users/login.html',
                'authentication_form': AuthenticationForm,
                'extra_context': {
                    'password_reset_url': '/%spassword_reset/' % conf.URL_PREFIX,
                    'login_url': login_url,
                    'next': login_redirect_url,
                    'login_view': True
                }
            },
            name=URLNAMES.login_urlname
        ),
        url(
            r'^%slogout/$' % conf.URL_PREFIX,
            _logout, logout_view_args,
            name=URLNAMES.logout_urlname
        ),
        # change password url; for users to change its own password.
        url(
            r'^%spassword_change/$' % conf.URL_PREFIX,
            password_change, {
                'template_name': 'users/password_change.html',
                'post_change_redirect': '/%spassword_change_done/' % conf.URL_PREFIX
            },
            name=URLNAMES.password_change_urlname
        ),
        # password change done url; displays confirmation.
        url(
            r'^%spassword_change_done/$' % conf.URL_PREFIX,
            password_change_done, {'template_name': 'users/password_change_done.html' },
            name=URLNAMES.password_change_done_urlname
        ),

        # account confirmation url, protected by secret token; displayed when the users clicked the account confirm url
        # in its account confirmation email
        url(
            r'^%saccount_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' % conf.URL_PREFIX,
            account_confirm, {
                'template_name': 'users/account_confirm.html',
                # after the account confirmation, the user gets redirected to the url defined in the settings
                'post_reset_redirect': settings.ACCOUNT_CONFIRM_REDIRECT_URL or '/%saccount_confirm_complete/' % conf.URL_PREFIX,
            },
            name=URLNAMES.account_confirm_urlname
        ),
        # indicated that the account was successfully confirmed
        url(
            r'^%saccount_confirm_complete/$' % conf.URL_PREFIX,
            TemplateView.as_view(
                template_name='users/account_confirm_complete.html',
            ),
            dict(
                login_redirect_url=login_redirect_url,
                login_url=login_url
             ),
            name=URLNAMES.account_confirm_complete_urlname
        ),

        # displays a form that takes a user's email address; when submitted, an email with a password reset url is sent
        # to that user
        url(
            r'^%spassword_reset/$' % conf.URL_PREFIX,
            password_reset, {
                'template_name': 'users/password_reset.html',
                'post_reset_redirect': '/%spassword_reset_done/' % conf.URL_PREFIX,
                'email_template_name': 'users/email/password_reset.html',
                'password_reset_form': get_password_reset_form(URLNAMES.password_reset_confirm_urlname, user_model),
            },
            name=URLNAMES.password_reset_urlname
        ),
        # displays that the password change email has been sent.
        url(
            r'^%spassword_reset_done/$' % conf.URL_PREFIX,
            password_reset_done, {
                'template_name': 'users/password_reset_done.html',
                'extra_context': {'login_url': login_url},
            },
            name=URLNAMES.password_reset_done_urlname
        ),
        # displays the form where the user can choose its new password
        url(
            r'^%spassword_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$' % conf.URL_PREFIX,
            password_reset_confirm, {
                'template_name': 'users/password_reset_confirm.html',
                'post_reset_redirect': '/%spassword_reset_complete/' % conf.URL_PREFIX,
            },
            name=URLNAMES.password_reset_confirm_urlname
        ),
        # indicates that the user's password has been successfuly changed.
        url(
            r'^%spassword_reset_complete/$' % conf.URL_PREFIX,
            password_reset_complete, {
                'template_name': 'users/password_reset_complete.html',
                'extra_context': {'login_url': login_url}
            },
            name=URLNAMES.password_reset_complete_urlname
        )
    ]
