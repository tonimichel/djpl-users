from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def refine_INSTALLED_APPS(original):
    return ['users'] + list(original)


refine_AUTHENTICATION_BACKENDS = ['users.auth_backend.AuthBackend', ]

introduce_IGNORE_USER_EMAIL = True
introduce_ADDITIONALLY_SEND_TO = []
introduce_LOGIN_URL = '/login/'
introduce_LOGIN_REDIRECT_URL = '/'
introduce_LOGOUT_REDIRECT_URL = '/login/'
introduce_ACCOUNT_CONFIRMATION_EMAIL_SUBJECT = _('Your Account')
