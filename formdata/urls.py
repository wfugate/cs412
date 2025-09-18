# File: urls.py
# Author: William Fugate wfugate@bu.edu
# Description: the list of urls for the quote of the day application
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.show_form, name="show_form"),
    path(r'submit', views.submit, name="submit"),

]
