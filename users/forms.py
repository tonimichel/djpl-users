# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as __


class AuthenticationForm(DjangoAuthForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label=__("Username"))


def get_user_form(modelclass):
    class UserForm(forms.ModelForm):
        email = forms.EmailField(required=True, label=_('Email'))
        first_name = forms.CharField(required=True, max_length=255, label=_('First name'))
        last_name = forms.CharField(required=True, max_length=255, label=_('Last name'))
        groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label=_('Groups'))

        class Meta:
            model = modelclass
            fields = ['email']

    return UserForm


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model


def get_password_reset_form(password_reset_confirm_urlname, ConcreteUserModel):
    class CustomPasswordResetForm(PasswordResetForm):

        def save(self, domain_override=None,
                 subject_template_name='registration/password_reset_subject.txt',
                 email_template_name='registration/password_reset_email.html',
                 use_https=False, token_generator=default_token_generator,
                 from_email=None, request=None, html_email_template_name=None):
            """
            Generates a one-use only link for resetting password and sends to the
            user.
            """
            UserModel = get_user_model()
            email = self.cleaned_data["email"]
            active_users = UserModel._default_manager.filter(
                email__iexact=email, is_active=True)

            for user in active_users:
                # Make sure that no email is sent to a user that actually has
                # a password marked as unusable
                if not user.has_usable_password():
                    continue

                # as we also want non users users to reset their password, we always
                # fake the concrete usermodel object.
                a = ConcreteUserModel(
                    username=user.username,
                    email=user.email,
                    last_login=user.last_login,
                    id=user.id,
                    is_active=user.is_active,
                    password=user.password,
                )
                a.pk = user.id
                a.confirm_account(template=email_template_name, subject='Passwort zurücksetzen')

    return CustomPasswordResetForm
