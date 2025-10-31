## voter_analytics/urls.py
## Author: William Fugate wfugate@bu.edu
## description: urls for the voter_analytics app
from .views import *
from django.urls import path
urlpatterns = [
    path('', VoterListView.as_view(), name='voters'), #default route shows all voters
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'), 
    path('graphs', GraphsView.as_view(), name='graphs'),

]