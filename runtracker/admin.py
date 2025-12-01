from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Run)
admin.site.register(UserProfile)
admin.site.register(Badge)
admin.site.register(Group)
admin.site.register(GroupMembership)

