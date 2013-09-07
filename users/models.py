# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site
from emailing.emails import HtmlEmail
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator

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
    
        
    def save(self, *args, **kwargs):
        updated = self.id

        if not updated:
            # set unsable password before the user is saved
            self.set_unusable_password()
        
        super(AbstractUser, self).save()
        
        if not updated and self.is_active:
            # send account confirmation mail after user was saved 
            self.confirm_account()
        
    def confirm_account(self):
        conf = self.AppConfig
        domain = getattr(conf, 'CONFIRM_LINK_TARGET_DOMAIN', False) or Site.objects.get(id=settings.SITE_ID).domain
        token = default_token_generator.make_token(self)
        uid = int_to_base36(self.id)
        bcc = conf.ADDITIONALLY_SEND_TO
        
        if conf.USE_USER_EMAIL:
            recipients = [self.email]
        else:
            recipients = bcc
            bcc = None
        
        email = HtmlEmail(
            from_email = conf.FROM_EMAIL,
            to = recipients,
            bcc = bcc,
            subject = conf.ACCOUNT_CONFIRM_EMAIL_SUBJECT,
            template = 'users/email/account_confirmation.html',
            context = {
                'token': token,
                'uid': uid,
                'user': self,
                'domain': domain,
                'account_confirm_url': '%s%s' % ( 
                    domain, 
                    reverse(conf.get_urlnames().account_confirm_urlname, kwargs={
                        'uidb36': uid,
                        'token': token
                    })
                )
            }
        )
        email.send()
        self.is_active = True
        self.save()
        
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    

class UserAppConfig(object):
    APP_LABEL = None 
    URL_PREFIX = None
    USER_MODEL = None 
    FROM_EMAIL = None 
    ACCOUNT_CONFIRM_EMAIL_TITLE = None
    CONFIRM_LINK_TARGET_DOMAIN = None
    LOGIN_URL = None
    LOGIN_REDIRECT_URL = None
    LOGOUT_REDIRECT_URL = None
    USE_USER_EMAIL = False,
    ADDITIONALLY_SEND_TO = []
    
    @classmethod
    def get_urlnames(cls):
        class __urlnames__(object):
            login_urlname = '%s-login' % cls.APP_LABEL
            logout_urlname = '%s-logout' % cls.APP_LABEL
            password_change_urlname = '%s-password_change' % cls.APP_LABEL
            password_change_done_urlname = '%s-password_change_done' % cls.APP_LABEL
            account_confirm_urlname = '%s-account_confirmation' % cls.APP_LABEL
            account_confirm_complete_urlname = '%s-account_confirm_complete' % cls.APP_LABEL
            password_reset_urlname = '%s-password_reset' % cls.APP_LABEL
            password_reset_done_urlname = '%s-password_reset_done' % cls.APP_LABEL
            password_reset_confirm_urlname = '%s-password_reset_confirm' % cls.APP_LABEL
            password_reset_complete_urlname = '%s-password_reset_complete' % cls.APP_LABEL
        return __urlnames__

       
    
    


