# File: urls.py
# Author: William Fugate wfugate@bu.edu
# Description: 
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'about', views.about, name="about_page"),
    path(r'', views.home_page, name="home_page"),

]
