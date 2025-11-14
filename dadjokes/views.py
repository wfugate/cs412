## dadjokes/views.py
## Author: Author: William Fugate wfugate@bu.edu
## description: views file for dad jokes app
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Joke, Picture
import random
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

class RandomView(TemplateView):
    """View for displaying a random Joke and Picture."""
    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs): #need to overwrite this method to add the joke and picture
        context = super().get_context_data(**kwargs)
        jokes = Joke.objects.all()
        pictures = Picture.objects.all()
        if jokes:
            context['joke'] = random.choice(jokes)
        if pictures:
            context['picture'] = random.choice(pictures)
        return context
    
class JokeListView(ListView):
    """View for displaying a list of Jokes."""
    model = Joke
    template_name = 'dadjokes/joke_list.html'
    context_object_name = 'jokes'
    ordering = ['-timestamp']

class PictureListView(ListView):
    """View for displaying a list of Pictures."""
    model = Picture
    template_name = 'dadjokes/picture_list.html'
    context_object_name = 'pictures'
    ordering = ['-timestamp']

class JokeDetailView(DetailView):
    """View for displaying details of a single Joke."""
    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'

class PictureDetailView(DetailView):
    """View for displaying details of a single Picture."""
    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'


class JokeListCreateAPIView(generics.ListCreateAPIView):
    """An API view to return a listing of Jokes or create a new Joke."""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to retrieve, update, or delete a Joke."""
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    """An API view to return a listing of Pictures."""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to retrieve, update, or delete a Picture."""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomJokeAPIView(APIView):
    """An API view to return a random Joke."""
    def get(self, request): #get method to return random joke
        jokes = list(Joke.objects.all())
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)

class RandomPictureAPIView(APIView):
    """An API view to return a random Picture."""
    def get(self, request): #get method to return random picture
        pictures = list(Picture.objects.all())
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)