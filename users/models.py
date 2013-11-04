# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as __
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.sites.models import Site
from emailing.emails import HtmlEmail
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError


class AbstractUser(User, models.Model):
    '''
    Defines an abstract user model which can be inherited and refined by a concrete application's user
    model.
    '''
    
    def __init__(self, *args, **kwargs):
        super(AbstractUser, self).__init__(*args, **kwargs)
        # make the email field (inherited from User) mandatory
        self._meta.get_field_by_name('email')[0].null = False
        self._meta.get_field_by_name('email')[0].blank = False
        self._meta.get_field_by_name('username')[0].max_length = 300 #FIXME: does not work on syncdb on postgres

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.username
    
        
    def save(self, send_confirmation=True):
        updated = self.id

        if not updated:
            # set unsable password before the user is saved
            self.set_unusable_password()
            self.is_staff = self.appconfig.IS_STAFF
        
        super(AbstractUser, self).save()
        
        if not updated and self.is_active and send_confirmation:
            # send account confirmation mail after user was saved 
            self.confirm_account()


        
    def confirm_account(self, template='users/email/account_confirmation.html', extra_context={}):
        conf = self.appconfig
        bcc = conf.ADDITIONALLY_SEND_TO
        
        if conf.USE_USER_EMAIL:
            recipients = [self.email]
        else:
            recipients = bcc
            bcc = None
            
        context = {
            'user': self,
            'account_confirm_url': self.get_account_confirm_link(self.urlnames.account_confirm_urlname)
        }
        context.update(extra_context)
        
        email = HtmlEmail(
            from_email = conf.FROM_EMAIL,
            to = recipients,
            bcc = bcc,
            subject = conf.CONFIRM_EMAIL_SUBJECT,
            template = template,
            context = context
        )
        email.send()
        self.is_active = True
        self.save()
        
    
    def get_account_confirm_link(self, urlname):
        domain = Site.objects.get(id=settings.SITE_ID).domain
        if not domain.startswith('http'):
            domain = 'http://' + domain
    
        return '%s%s' % (
            domain, 
            reverse(urlname, kwargs={
                'uidb36': int_to_base36(self.id),
                'token':  default_token_generator.make_token(self)
            })
        )
    
        
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
        
    
    def clean(self):
        
        if self.id:
            u = User.objects.get(id=self.id)
    
        if User.objects.filter(username=self.email).exclude(email=u.email).count() > 0:
            raise ValidationError(_('A user with that email already exists.'))
    

       
    
    


