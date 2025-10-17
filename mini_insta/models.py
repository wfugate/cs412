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
    
    def get_followers(self):
        '''Returns all profiles that follow this profile.'''
        return list(Follow.objects.filter(profile=self))
    
    def get_num_followers(self):
        '''Returns the number of followers this profile has.'''
        return len(self.get_followers())
    
    def get_following(self):
        '''Returns all profiles that this profile is following.'''
        return list(Follow.objects.filter(follower_profile=self))
    
    def get_num_following(self):
        '''Returns the number of profiles this profile is following.'''
        return len(self.get_following())

    def get_post_feed(self):
        '''Returns a feed of posts from profiles this profile is following.'''
        following = self.get_following()
        feed_posts = Post.objects.filter(profile__in=[f.profile for f in following]).order_by('-timestamp') #filter posts by profiles being followed
        return feed_posts
    

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
    
    def get_all_comments(self):
        '''Returns all comments made on this post.'''
        return Comment.objects.filter(post=self).order_by('timestamp')
    
    def get_likes(self):
        '''Returns all likes made on this post.'''
        return Like.objects.filter(post=self)

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
        
class Follow(models.Model):
    '''Model representing a follow relationship between two profiles in the mini insta application.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='propfile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"
    

class Comment(models.Model):
    '''Model representing a comment made on a post in the mini insta application.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.profile.display_name} on post {self.post.id}"
    
class Like(models.Model):
    '''Model representing a like made on a post in the mini insta application.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.profile.display_name} on {self.post}"
    

    
