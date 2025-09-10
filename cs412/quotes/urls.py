# File: urls.py
# Author: William Fugate wfugate@bu.edu
# Description: the list of urls for the quote of the day application
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'quote', views.quote_page, name="quote_page"),
    path(r'show_all', views.show_all_page, name="show_all_page"),
    path(r'about', views.about_page, name="about_page"),

]
