from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from emailing.emails import HtmlEmail


def send_confirmation_mail(user, template, extra_context, subject):
    if not extra_context:
        extra_context = dict()

    conf = user.appconfig
    bcc = settings.ADDITIONALLY_SEND_TO
    subject = subject or conf.CONFIRM_EMAIL_SUBJECT

    if settings.IGNORE_USER_EMAIL:
        recipients = bcc
        bcc = None
    else:
        recipients = [user.email]

    token = default_token_generator.make_token(user)
    context = {
        'user': user,
        'password_reset_confirm_url': user.get_confirm_link(user.urlnames.password_reset_confirm_urlname, token),
        'account_confirm_url': user.get_confirm_link(user.urlnames.account_confirm_urlname, token),
        'login_url': user._get_domain() + settings.LOGIN_URL
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
