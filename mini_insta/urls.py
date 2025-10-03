## mini_insta/urls.py
## Author: Author: William Fugate wfugate@bu.edu
## description: urls for mini_insta app
from django.urls import path
from .views import ProfileListView
from .views import ProfileDetailView, PostDetailView, CreatePostView
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'), #default route shows all profiles
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'), #route to show a specific profile by primary key
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'), #route to show a specific post by primary key
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'), #route to create a new post
]

