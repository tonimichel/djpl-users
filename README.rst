django-users
====================================

A django-productline feature to enable user functionality for non-admin multiuser scenarios.
Builds upon django.auth and provides signup, confirmation email, and password reset functionality.



Installation
====================================

1) clone this repo e.g.: ``git clone https://github.com/tonimichel/django-users.git`` and cd into it.


2) Install the python package::

    python setup.py install


Usage
===================================

*users* provides an abstract model and some urlpatterns which allow you to
create custom user models for your app featuring:

* confirmation emails when a user is created
* password reset process when a user forgot his password
* admin actions to manually send confirmation emails

The users feature is designed for scenarios where you have a user base and dont want
to set or reset each user's password manually. You might use it in admin scenarios
or non-admin scenarios.

The usage is quite easy and can be accomplished in 3 steps:

1) Create your own user model extending AbstractUser and add the inner class AppConfig
2) Add the urlpatterns by using users.authurls.get_patterns(FooUser)
3) Set the necessary email properties in your settings.py

As this is a django-productline feature, make sure you have users in your product.equation



models.py
----------------

Just extend AbstractUser and specify your AppConfig.

.. code-block:: python

    from django.db import models
    from users.models import AbstractUser, UserAppConfig
    
    class FooUser(AbstractUser):
        
        someadditionalfield = models.CharField(max_length=255)
        
        class AppConfig(UserAppConfig):
            APP_LABEL = 'myappname' # used for prefixing the urlnames 
            URL_PREFIX = 'myurlprefix' # all users urls are prefixed with that string
            FROM_EMAIL = 'system@schnapptack.de' # your from email
            ACCOUNT_CONFIRM_EMAIL_SUBJECT = 'your new FooApp account' # the subject of the email 
            CONFIRM_LINK_TARGET_DOMAIN = 'http://example.com' # the domain used for the activation link in the activation email
            LOGIN_URL = 'login/' # the login url relative to the URL_PREFIX
            LOGIN_REDIRECT_URL = '/' 
            LOGOUT_REDIRECT_URL = '/ciao/'
            USE_USER_EMAIL = False, # indicate whether to use the email of this user or not; for debugging set to false;
            ADDITIONALLY_SEND_TO = [] # additionally send these emails to
        

urlpatterns
-----------------

.. code-block:: python

    from users import authurls
    from foo.models import FooUser
    
    ...
    
    urlpatterns += authurls.get_patterns(FooUser)



admin.py
-----------------

.. code-block:: python

    from django.contrib import admin
    from users.admin import UserAdmin
    from foo.models import FooUser
    
    class FooUserAdmin(UserAdmin):
        pass
        
        
    admin.site.register(FooUser, FooUserAdmin)
    



License
========

MIT
