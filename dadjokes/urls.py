## dadjokes/urls.py
## Author: Author: William Fugate wfugate@bu.edu
## description: urls for dad jokes app
from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomView.as_view(), name='home'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture_detail'),
    path('', RandomView.as_view(), name='home'),
    path('random', RandomView.as_view(), name='random'),
    path('jokes', JokeListView.as_view(), name='jokes'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', PictureListView.as_view(), name='pictures'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture_detail'),
    path('api/', RandomJokeAPIView.as_view(), name='api_random'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/jokes', JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),
]

