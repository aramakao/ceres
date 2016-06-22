from django.contrib import admin
from .models import *

admin.site.register(Group)
admin.site.register(GroupProfile)
admin.site.register(GroupMember)
admin.site.register(StateGroup)
admin.site.register(StateGroupComment)
admin.site.register(InivitationGroup)
