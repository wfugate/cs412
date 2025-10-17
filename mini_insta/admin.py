## mini_insta/admin.py
## Author: William Fugate
## description: admin configuration file for mini_insta app
from django.contrib import admin

from .models import *


admin.site.register(Profile) #register the Profile model with the admin site
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)