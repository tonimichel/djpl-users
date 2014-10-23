from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as __
from django.utils.translation import ugettext as _
from django.utils.http import int_to_base36
from django.core.urlresolvers import reverse
from emailing.emails import HtmlEmail
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm
from django.contrib.auth.models import Group

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





  
