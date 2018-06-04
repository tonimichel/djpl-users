


def register(modelclass, config):
    from users import authurls
    app_label = 'users'
    
    class __urlnames__(object):
        login_urlname = '%s-login' % app_label
        logout_urlname = '%s-logout' % app_label
        password_change_urlname = '%s-password_change' % app_label
        password_change_done_urlname = '%s-password_change_done' % app_label
        account_confirm_urlname = '%s-account_confirm' % app_label
        account_confirm_complete_urlname = '%s-account_confirm_complete' % app_label
        password_reset_urlname = '%s-password_reset' % app_label
        password_reset_done_urlname = '%s-password_reset_done' % app_label
        password_reset_confirm_urlname = '%s-password_reset_confirm' % app_label
        password_reset_complete_urlname = '%s-password_reset_complete' % app_label
    

    
    # set appconfig defaults
    class __appconfig__(object):
        IS_STAFF = False
        
    for key, value in config.items():
        setattr(__appconfig__, key, value)
        
    setattr(modelclass, 'appconfig', __appconfig__)
    setattr(modelclass, 'urlnames', __urlnames__)
    
    URLPATTERNS = authurls.get_patterns(modelclass)

    @classmethod
    def get_urlpatterns(cls):
        return URLPATTERNS
        
    setattr(modelclass, 'get_urlpatterns', get_urlpatterns)
