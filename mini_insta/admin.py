## mini_insta/admin.py
## Author: William Fugate
## description: admin configuration file for mini_insta app
from django.contrib import admin
from .models import Profile


admin.site.register(Profile) #register the Profile model with the admin site