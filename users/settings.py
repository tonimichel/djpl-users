


def refine_INSTALLED_APPS(original):
    return ['users'] + list(original)
    
    

introduce_IGNORE_USER_EMAIL = False
introduce_ADDITIONALLY_SEND_TO = []

introduce_LOGIN_URL = '/login/'
introduce_LOGIN_REDIRECT_URL = '/'
introduce_LOGOUT_REDIRECT_URL = '/login/'
