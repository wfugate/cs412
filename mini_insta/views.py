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
        form.instance.profile = profile #adding profile to the form instance to be saved
        response = super().form_valid(form)
        
        images = self.request.FILES.getlist('image_file') #get the list of uploaded images
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
        context = super().get_context_data(**kwargs) #get the default context data
        context['post'] = self.object #add the post being deleted to the context
        context['profile'] = self.object.profile #add the profile owning the post to the context
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
        context = super().get_context_data(**kwargs) #get the default context data
        context['post'] = self.object #add the post being updated to the context
        context['profile'] = self.object.profile #add the profile owning the post to the context
        return context
    
    def get_success_url(self):
        '''Redirect to the post detail page after updating.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
class ShowFollowersDetailView(DetailView):
    '''View to see a Profile's followers.'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''View to see who a Profile is following.'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']

    def get_queryset(self):
        """Return the post feed for the profile with this pk."""
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk) #filter by profile pk
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the profile to the template context."""
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs.get('pk')
        context['profile'] = Profile.objects.get(pk=profile_pk) #add the profile to the context
        return context
    
class SearchView(ListView):
    '''View to search profiles and posts.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Check if query is present, if not show search form.'''
        if 'query' not in self.request.GET: #show the search form if no query
            profile_pk = self.kwargs.get('pk')
            profile = Profile.objects.get(pk=profile_pk) #get the profile by pk
            return render(request, 'mini_insta/search.html', {'profile': profile})
        else:
            return super().dispatch(request, *args, **kwargs) #continue with ListView processing if there is a query

    def get_queryset(self):
        '''Return posts matching the search query.'''
        query = self.request.GET.get('query', '') #get the search query
        if query:
            return Post.objects.filter(caption__icontains=query).order_by('-timestamp') #if theres a search query, filter posts by caption
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        '''Add profile, query, posts, and matching profiles to context.'''
        context = super().get_context_data(**kwargs)
        
        #get the profile
        profile_pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        
        #get the query
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        #get matching profiles
        if query:
            #combine results from all three fields
            username_matches = Profile.objects.filter(username__icontains=query)
            display_name_matches = Profile.objects.filter(display_name__icontains=query)
            bio_matches = Profile.objects.filter(bio_text__icontains=query)
            
            #union of all matches (also remove duplicates with distinct())
            profiles = (username_matches | display_name_matches | bio_matches).distinct()
            context['profiles'] = profiles
        else:
            context['profiles'] = Profile.objects.none()
        
        return context