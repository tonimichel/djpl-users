



def refine_get_urls(original):

    def get_urls():
        from django.contrib.auth.decorators import login_required
        from django.contrib import admin
        
        # wrap the default admin login view with the login_required decorators
        # so that settings.LOGIN_URL is used
        admin.site.login = login_required(admin.site.login)
                
        return original()
    return get_urls



