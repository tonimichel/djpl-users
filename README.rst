djpl-users
====================================

A django-productline feature to enable user functionality for non-admin multiuser scenarios.
Builds upon django.auth and provides signup, confirmation email, and password reset functionality.


This is a django-productline feature: https://django-productline.readthedocs.org/en/latest/


Installation
====================================

pip install -e git+https://github.com/tonimichel/djpl-users.git#egg=djpl-users
    


Usage
===================================

*users* provides an abstract model and urlpatterns to enable custom user models
featuring:

* confirmation emails when a user is created
* password reset process when a user forgot his password
* admin actions to manually send confirmation emails

The users feature is designed for scenarios where you have a user base and dont want
to set or reset each user's password manually. You can use it in admin scenarios
or non-admin scenarios.

Integrating djpl-users can be accomplished in 4 steps:

1) Add ``users`` to your ``settings.INSTALLED_APPS`` or add the feature to your product
2) Create your own user model extending ``AbstractUser``
3) Register your custom user model *users.register(modelclass, config)*
4) Add the urlpatterns (usermodel.get_urlpatterns)

As the feature sends emails, be sure to introduce the necessary email server configuration in your settings.


Your models
----------------

Just extend AbstractUser and register your new model.

.. code-block:: python

    from django.db import models
    from users.models import AbstractUser
    import users

    class FooUser(AbstractUser):

        someadditionalfield = models.CharField(max_length=255)

    users.register(FooUser, dict(
        APP_LABEL = 'myappname', # used for prefixing the urlnames
        URL_PREFIX = 'myurlprefix', # all users urls are prefixed with that string
        FROM_EMAIL = 'info@schnapptack.de', # your from email
        CONFIRM_EMAIL_SUBJECT = 'your new FooApp account', # the subject of the email
        LOGIN_URL = 'login/', # the login url relative to the URL_PREFIX
        LOGIN_REDIRECT_URL = '/',
        LOGOUT_REDIRECT_URL = '/ciao/',
        USE_USER_EMAIL = False, # indicate whether to use the email of this user or not; for debugging set to false;
        ADDITIONALLY_SEND_TO = [], # additionally send these emails to
    ))


Your urlpatterns
-----------------

.. code-block:: python

    from foo.models import FooUser

    ...

    urlpatterns += FooUser.get_urlpatterns()



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
