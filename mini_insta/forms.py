## mini_insta/forms.py
## Author: Author: William Fugate wfugate@bu.edu
## description: forms.py for mini_insta app
from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']




