from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Model representing a user profile in the mini insta application.'''
    username = models.CharField()
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
