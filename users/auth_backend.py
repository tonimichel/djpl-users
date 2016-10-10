# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class AuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        """
        Ensures case insensitive user names and checks against username and email in order
        allow email as login credential.
        :param username:
        :param password:
        :return:
        """
        user = None
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            # alternatively check against the email
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                pass

        if user is not None and user.check_password(password):
            return user
