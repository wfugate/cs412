## dadjokes/models.py
## Author: Author: William Fugate wfugate@bu.edu
## description: model definitions for dadjokes app
from django.db import models

class Joke(models.Model):
    text = models.TextField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contributor}'s Joke"

class Picture(models.Model):
    image_url = models.TextField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.contributor}'s Photo"
