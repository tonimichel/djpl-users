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

from django.contrib.auth.forms import AuthenticationForm as DjangoAuthForm

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
        class Meta:
            model = modelclass
            
    return UserForm


def get_password_reset_form(password_reset_confirm_urlname):

    class PasswordResetForm(forms.Form):
        email = forms.EmailField(label=_("Email"), max_length=75)

        def clean_email(self):
            """
            Validates that an active user exists with the given e-mail address.
            """
            email = self.cleaned_data["email"]
            self.users_cache = User.objects.filter(
                                    email__iexact=email,
                                    is_active=True
                                )
            if len(self.users_cache) == 0:
                raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
            return email

        def save(self, domain_override=None, 
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.html',
            use_https=False, 
            token_generator=default_token_generator, 
            from_email=None, 
            request=None):
            """
            Generates a one-use only link for resetting password and sends to the user
            """
            from django.core.mail import send_mail
            for user in self.users_cache:
                if not domain_override:
                    current_site = get_current_site(request)
                    site_name = current_site.name
                    domain = current_site.domain
                else:
                    site_name = domain = domain_override
                
                c = {
                    'email': user.email,
                    'domain': domain,
                    'site_name': site_name,
                    'user': user,
                    'protocol': use_https and 'https' or 'http',
                    'password_reset_confirm_url': '%s%s' % ( 
                            domain, 
                            reverse(password_reset_confirm_urlname, kwargs={'uidb36':int_to_base36(user.id), 'token': token_generator.make_token(user) })
                    )
                }
                
                subject = loader.render_to_string(subject_template_name, c)
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                
                email = HtmlEmail(
                    from_email = from_email,
                    to = [user.email],
                    subject = subject, #_("Password reset on %s") % site_name,
                    template = email_template_name,
                    context = c
                )
                email.send()
                
    return PasswordResetForm          




  
