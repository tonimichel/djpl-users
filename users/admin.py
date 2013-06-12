from django.contrib import admin
from django.conf.urls.defaults import url, patterns, include
from django.utils.translation import ugettext as _
from users.forms import get_user_form




class UserAdmin(admin.ModelAdmin):
    
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.form = get_user_form(self.model)
    
    fieldsets=[
         ('main', {
            'fields': ('username', 'email',  'is_active')
        }),
    ]
   
    actions = ['set_active', 'set_inactive', 'send_account_confirmation']
   
    def set_active(self, request, queryset):
        queryset.update(is_active=True)
    set_active.short_description = _('Mark selected users as active')

    def set_inactive(self, request, queryset):
        queryset.update(is_active=False)
    set_inactive.short_description = _('Mark selected users as inactive')

    def send_account_confirmation(self, request, queryset):
        for user in queryset:
            user.confirm_account()
    send_account_confirmation.short_description = _('Send account confirmation email to selected users')

   
   
   
   
class UserSelfAdmin(admin.ModelAdmin):
    fieldsets=[
         ('main', {
            'fields': ('email', )
        }),
    ]

    def add_view(self, request, form_url='', extra_context=None):
        return self.change_view(request, request.user.id)
        
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(AbstractUserSelfAdmin, self).change_view(request, request.user.id, form_url=form_url, extra_context=extra_context)



