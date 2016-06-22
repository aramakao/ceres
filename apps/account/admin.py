from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(StateUser)
admin.site.register(StateUserComment)
admin.site.register(StateUserLike)
admin.site.register(Friend)
admin.site.register(InivitationFriend)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','last_name','email')
    search_fields=('username','email')
    list_filter=('is_superuser',)
    ordering=('username',)
    filter_horizontal=('groups','user_permissions')
    fieldsets=(
        ('User',{'fields':('username','password')}),
        ('Personal Info',{'fields':(
            'first_name',
            'last_name',
            'email',
            'avatar',
        )}),
        ('Permissions',{'fields':(
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
    )


from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
