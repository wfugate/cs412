## mini_insta/views.py
## Author: William Fugate wfugate@bu.edu
## description: views.py for mini_insta app
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile, Post, Photo
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .forms import UpdateProfileForm, UpdatePostForm



class ProfileListView(ListView):
    '''View to see all profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''View to see a profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'


class PostDetailView(DetailView):
    '''View to see a Post.'''
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
        
        images = self.request.FILES.getlist('image_file')
        for image in images:
            photo = Photo(post=self.object, image_file = image)
            photo.save()
        
        return response
    
class UpdateProfileView(UpdateView):
    '''View to update a post.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'


class DeletePostView(DeleteView):
    '''View to delete a post.'''
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    
    def get_context_data(self, **kwargs):
        '''Add post and profile to the template context.'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        '''Redirect to the profile page after deleting the post.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class UpdatePostView(UpdateView):
    '''View to update a post'''
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add post and profile to the template context.'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        '''Redirect to the post detail page after updating.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
