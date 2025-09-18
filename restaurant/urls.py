from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'confirmation', views.confirmation, name="confirmation"),
    path(r'order', views.order, name="order"),
    path(r'main', views.main, name="main"),
    path(r'', views.main, name="main" )

]