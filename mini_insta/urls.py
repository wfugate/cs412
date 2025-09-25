## mini_insta/urls.py
## Author: William Fugate
## description: urls for mini_insta app
from django.urls import path
from .views import ProfileListView
from .views import ProfileDetailView
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'), #default route shows all profiles
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'), #route to show a specific profile by primary key
    
]

