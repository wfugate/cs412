## mini_insta/urls.py
## Author: Author: William Fugate wfugate@bu.edu
## description: urls for mini_insta app
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'), #default route shows all profiles
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'), #route to show a specific profile by primary key
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'), #route to show a specific post by primary key
    path('profile/create_post', CreatePostView.as_view(), name='create_post'), #route to create a new post
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), #route to update a profile
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'), #route to delete a post
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'), #route to update a post
    path('profile/<int:pk>/following', ShowFollowersDetailView.as_view(), name='show_followers'), #route to show followers of a profile
    path('profile/<int:pk>/followers', ShowFollowingDetailView.as_view(), name='show_following'), #route to show following of a profile
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'), #route to show post feed of a profile
    path('profile/search', SearchView.as_view(), name='search'), #route to search for profiles and posts
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'), #route to login page
	path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'), #route to logout page
    path('logged_out/', LoggedOutView.as_view(), name='logged_out'), #route to logged out page
    path('create_profile', CreateProfileView.as_view(), name='create_profile'), #route to create a new profile
    path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow_profile'), #route to follow a profile
    path('profile/<int:pk>/delete_follow', DeleteFollowView.as_view(), name='delete_follow'), #route to unfollow a profile
    path('post/<int:pk>/like', LikePostView.as_view(), name='like_post'), #route to like a post
    path('post/<int:pk>/delete_like', DeleteLikeView.as_view(), name='delete_like'), #route to unlike a post
]

