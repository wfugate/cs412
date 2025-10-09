## mini_insta/forms.py
## Author: Author: William Fugate wfugate@bu.edu
## description: forms.py for mini_insta app
from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    '''Form for creating a post.'''
    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''Form for updating a profile.'''
    class Meta:
        model = Profile
        fields = ['bio_text', 'display_name', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    '''Form for updating a post.'''
    class Meta:
        model = Post
        fields = ['caption']




