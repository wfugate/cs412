## mini_insta/views.py
## Author: William Fugate wfugate@bu.edu
## description: views.py for mini_insta app
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile, Post, Photo
from django.views.generic import DetailView, CreateView
from django.urls import reverse



class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'


class PostDetailView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    model = Post
    template_name = 'mini_insta/create_post_form.html'
    fields = ['caption']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        '''Add the profile pk to the template context.'''
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
    def form_valid(self, form):
        '''Set the profile for the post before saving and create associated photo.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        response = super().form_valid(form)
        
        image_url = self.request.POST.get('image_url')
        if image_url:
            photo = Photo(post=self.object, image_url=image_url)
            photo.save()
        
        return response

