from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User




class AuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        '''
        Ensures case insensitive user names.
        '''
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
