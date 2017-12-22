from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _
from emailing.emails import HtmlEmail


@python_2_unicode_compatible
class AbstractUser(User):
    """
    Defines an abstract user model which can be inherited and refined by a concrete application's user
    model.
    """

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(AbstractUser, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def __str__(self):
        if self.first_name and self.last_name:
            return '{first_name} {last_name}'.format(first_name=self.first_name, last_name=self.last_name)
        else:
            return self.email

    def save(self, send_confirmation=True, password=None, *args, **kw):
        """
        Saves the user instance and sends out a confirmation email on create.
        :param send_confirmation: boolean
        :param password: string
        :param args: list
        :param kw: dict
        :return: None
        """
        self.clean()

        updated = self.id

        if not updated:

            if not password:
                # set unusable password before the user is saved in case no password was
                # passed
                self.set_unusable_password()
            else:
                self.set_password(password)

            self.is_staff = self.appconfig.IS_STAFF
            # in case no username is passed, set a uuid

            if self.username in ('', None):
                # set username to a uuid in case it is not set which may happen
                # if you use self.email as username;
                # remeber: you now can login with your username (for backwards comp)
                # or with your email (see auth_backend).
                self.username = uuid.uuid4().hex[:30]

        self.username = self.username.lower()
        super(AbstractUser, self).save(*args, **kw)

        if not updated and self.is_active and send_confirmation:
            # send account confirmation mail after user was saved
            self.confirm_account()

    def clean(self):
        """
        Ensure that this instance does not violate our email unique constraint.
        :return:
        """
        qs = User.objects.filter(email__iexact=self.email)

        if self.id:
            # exclude this instance in case of update.
            qs = qs.exclude(id=self.id)

        if qs.count() > 0:
            raise ValidationError(dict(email=_('A user with this email (%s) already exists.' % self.email.lower())))

    def confirm_account(self, template='users/email/account_confirmation.html', extra_context=None, subject=None):
        """
        Sends out an account confirm email. Which contains a link to set the user's password.
        This method is also used for the password_reset mechanism.
        :param template:
        :param extra_context:
        :param subject:
        :return:
        """
        if not extra_context:
            extra_context = dict()

        conf = self.appconfig
        bcc = settings.ADDITIONALLY_SEND_TO
        subject = subject or conf.CONFIRM_EMAIL_SUBJECT

        if settings.IGNORE_USER_EMAIL:
            recipients = bcc
            bcc = None
        else:
            recipients = [self.email]

        token = default_token_generator.make_token(self)
        context = {
            'user': self,
            'password_reset_confirm_url': self.get_confirm_link(self.urlnames.password_reset_confirm_urlname, token),
            'account_confirm_url': self.get_confirm_link(self.urlnames.account_confirm_urlname, token),
            'login_url': self._get_domain() + settings.LOGIN_URL
        }
        context.update(extra_context)
        email = HtmlEmail(
            from_email=conf.FROM_EMAIL,
            to=recipients,
            bcc=bcc,
            subject=subject,
            template=template,
            context=context
        )
        email.send()

    def get_confirm_link(self, urlname, token):
        return '%s%s' % (
            self._get_domain(),
            reverse(urlname, kwargs={
                'uidb64': str(urlsafe_base64_encode(force_bytes(self.id)), 'utf-8'),
                'token': token
            })
        )

    def _get_domain(self):
        """
        Returns the domain from the Site model and prepends http.
        :return:
        """
        domain = Site.objects.get(id=settings.SITE_ID).domain
        if not domain.startswith('http'):
            domain = 'http://' + domain
        return domain

    def full_name(self):
        """
        Returns the full name of the user
        :return: string
        """
        return '%s %s' % (self.first_name, self.last_name)
