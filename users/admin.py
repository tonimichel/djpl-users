from django.contrib import admin
from django.conf.urls.defaults import url, patterns, include
from django.utils.translation import ugettext as _
from users.forms import get_user_form
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.admin import actions



class UserAdmin(admin.ModelAdmin):
    
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.form = get_user_form(self.model)
    
    
    fieldsets=[
        (_('User data'), {
            'fields': ('first_name', 'last_name')
        }),
        (_('Credentials'), {
            'fields': ('username', 'email',  'is_active')
        }),
    ]
   
    actions = ['set_active', 'set_inactive', 'send_account_confirmation', 'delete_selected']
    list_display = ['username', 'date_joined', 'is_active']
   
   
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


    # -----------------------
    # the following methods are to prevent a user from deleting himself.

    def delete_model(self, request, obj):
        '''
        Only deletes ``obj`` in case it is not the current user.
        '''
        if self.get_auth_user(request.user).id == self.get_auth_user(obj).id:
            messages.error(request, _('You cannot delete yourself!'))
            return
        else:
            obj.delete()
            
    def delete_selected(self, request, queryset):
        '''
        Remove the current user from the queryset selection and redirect to
        the changelist in case it was the only one.
        '''        
        me = self.get_auth_user(request.user)
        me_id = None
        for obj in queryset:
            if self.get_auth_user(obj).id == me.id:
                me_id = me.id
        queryset = queryset.exclude(id=me_id)
        
        if len(queryset):
            if me_id != None:
                messages.error(request, _('You cannot delete yourself! Removed you from selection.'))
            return actions.delete_selected(self, request, queryset)
        else:
            messages.error(request, _('You cannot delete yourself!'))
            return None
         
    delete_selected.short_description = "Delete selected"
    
    
    def get_auth_user(self, user_obj):
        '''
        This method always returns the auth user object from a given ``user_obj``.
        ``user_obj`` might be a child model of the original auth user.
        '''
        if hasattr(user_obj, 'user_ptr'):
            return user_obj.user_ptr
        else:
            return user_obj
        
    def delete_view(self, request, object_id, extra_context=None):
        '''
        Ensure that a user can never delete himself.
        As the concrete user model is child of the auth user, the current user
        requires delete permissions. However this "parent" permissions are only required for delete.
        '''
        if self.get_auth_user(request.user).id == self.get_auth_user(get_object_or_404(self.model, pk=object_id)).id:
            messages.error(request, _('You cannot delete yourself!'))
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model.__name__.lower())))
        else:
            return super(UserAdmin, self).delete_view(request, object_id, extra_context=None)

   
   
   
   
class UserSelfAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']

    def add_view(self, request, form_url='', extra_context=None):
        return HttpResponseRedirect(reverse('admin:%s_%s_change' % self.model._meta.app_label, self.model.__class__.__name__, args=[request.user.id]))
        
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        
        extra_context = extra_context or {}
        extra_context['title'] = 'My Profile'
    
        return super(UserSelfAdmin, self).change_view(request, str(request.user.id), form_url=form_url, extra_context=extra_context)
        
        
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model.__name__.lower()), args=[request.user.id]))



