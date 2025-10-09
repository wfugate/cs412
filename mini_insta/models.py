## mini_insta/models.py
## Author: William Fugate
## description: data models for mini_insta app
from django.db import models
from django.urls import reverse

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
    
    def get_all_posts(self):
        '''Returns all posts made by this profile.'''
        return Post.objects.filter(profile=self)
    
    def get_absolute_url(self):
        '''Returns the URL to access this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class Post(models.Model):
    '''Model representing a post made by a user in the mini insta application.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.profile.username} at {self.timestamp}"
    
    def get_all_photos(self):
        '''Returns all photos associated with this post.'''
        return Photo.objects.filter(post=self).order_by('timestamp')
    
    def get_absolute_url(self):
        '''Returns the URL to access this post.'''
        return reverse('show_post', kwargs={'pk': self.pk})

class Photo(models.Model):
    '''Model representing a photo associated with a post in the mini insta application.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for post {self.post.id}"
    
    def get_image_url(self):
        '''Returns an image's URL'''
        if (self.image_file):
            return self.image_file.url
        else:
            return self.image_url