## runtracker/urls.py
## Author: William Fugate wfugate@bu.edu
## description: url pattern definition for runtracker app
from django.urls import path
from .views import *

urlpatterns = [
    path('runs/', RunListCreateAPIView.as_view(), name='run-list-create'),
    path('runs/<int:pk>/', RunDetailAPIView.as_view(), name='run-detail'),
    path('profile/<int:user__id>/', UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('runs/<int:run_id>/nearby/', RunProximitySearchAPIView.as_view(), name='run-proximity'),
    path('profile/<int:user__id>/', UserProfileDetailAPIView.as_view(), name='profile-detail'),
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/members/', GroupMembersListAPIView.as_view(), name='group-member-list'),
    path('groups/<int:group_id>/members/add/', GroupAddMemberAPIView.as_view(), name='group-member-add'),
    path('groups/<int:group_id>/members/<int:user_id>/remove/', GroupRemoveMemberAPIView.as_view(), name='group-member-remove'),
    path('badges/', BadgeListAPIView.as_view(), name='badge-list'),
    path('badges/<int:pk>/', BadgeDetailAPIView.as_view(), name='badge-detail'),
]