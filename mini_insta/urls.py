## mini_insta/urls.py
## Author: Author: William Fugate wfugate@bu.edu
## description: urls for mini_insta app
from django.urls import path
from .views import ProfileListView
from .views import ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'), #default route shows all profiles
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'), #route to show a specific profile by primary key
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'), #route to show a specific post by primary key
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name='create_post'), #route to create a new post
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/following', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/followers', ShowFollowingDetailView.as_view(), name='show_following'),
]

