## voter_analytics/admin.py
## Author: William Fugate wfugate@bu.edu
## description: admin registration of models for voter_analytics
from django.contrib import admin
from .models import Voter

admin.site.register(Voter) 