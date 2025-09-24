from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.main_page, name="main_page"),
    path(r'submit', views.submit_page, name="submit_page"),
    
]