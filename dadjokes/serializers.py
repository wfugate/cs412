## dadjokes/serializers.py
## Author: Author: William Fugate wfugate@bu.edu
## description: serializers for the dadjokes app
from rest_framework import serializers
from .models import Joke, Picture

#serializer for Joke model
class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']

#serializer for Picture model
class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'timestamp']