## mini_insta/views.py
## Author: William Fugate wfugate@bu.edu
## description: views.py for mini_insta app
from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile, Post, Photo, Like, Follow, Comment
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from .forms import UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect


class ProfileRequiredMixin(LoginRequiredMixin):
    '''Mixin to ensure the user is logged in to access profile-related views.'''
    def get_profile(self):
        '''Get the profile associated with the logged-in user.'''
        return self.request.user.profile
    
    def get_login_url(self):
        '''Return the login URL.'''
        return reverse('login')

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

    def get_context_data(self, **kwargs):
        '''Add the whether the logged-in user is viewing their own profile to the context.'''
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            context['is_owner'] = (user_profile == profile)
            context['is_following'] = Follow.objects.filter(
                follower_profile=user_profile,
                profile=profile
            ).exists()
        else:
            context['is_owner'] = False
            context['is_following'] = False
        return context


class PostDetailView(DetailView):
    '''View to see a Post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Add is_owner to the template context.'''
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.get(user=self.request.user)
            context['is_owner'] = (user_profile == post.profile)

            context['has_liked'] = Like.objects.filter(
                profile=user_profile,
                post=post
            ).exists()
        else:
            context['is_owner'] = False
            context['has_liked'] = False
        return context
class CreatePostView(ProfileRequiredMixin, CreateView):
    model = Post
    template_name = 'mini_insta/create_post_form.html'
    fields = ['caption']

    def get_success_url(self):
        profile = self.get_profile()
        pk = profile.pk
        return reverse('show_profile', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        '''Add the profile pk to the template context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context
    
    def form_valid(self, form):
        '''Set the profile for the post before saving and create associated photo.'''
        profile = self.get_profile()
        form.instance.profile = profile #adding profile to the form instance to be saved
        response = super().form_valid(form)
        
        images = self.request.FILES.getlist('image_file') #get the list of uploaded images
        for image in images:
            photo = Photo(post=self.object, image_file = image)
            photo.save()
        
        return response
    
class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    '''View to update a post.'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''Return the profile of the logged-in user.'''
        return self.get_profile()


class DeletePostView(ProfileRequiredMixin, DeleteView):
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
        return reverse('show_profile', kwargs={'pk': self.get_profile().pk})
    
class UpdatePostView(ProfileRequiredMixin, UpdateView):
    '''View to update a post'''
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        '''Add post and profile to the template context.'''
        context = super().get_context_data(**kwargs) #get the default context data
        context['post'] = self.object #add the post being updated to the context
        context['profile'] = self.get_profile() #add the profile owning the post to the context
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

class PostFeedListView(ProfileRequiredMixin, ListView):
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']

    def get_queryset(self):
        '''Return the post feed for the logged-in user's profile.'''
        profile = self.get_profile() #get the profile of the logged-in user
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add profile to the template context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()  #add the profile to the context
        return context
    
class SearchView(ProfileRequiredMixin, ListView):
    '''View to search profiles and posts.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Check if query is present, if not show search form.'''
        if 'query' not in self.request.GET: #show the search form if no query
            profile = self.get_profile()
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
        profile = self.get_profile()
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
    
class LoggedOutView(TemplateView):
    '''View to show logout confirmation.'''
    template_name = 'mini_insta/logged_out.html'

class CreateProfileView(CreateView):
    '''View to create a profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        '''Add any additional context if needed.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()  #add a user creation form to the context
        return context
    def form_valid(self, form):
        '''Create the associated User object before saving the Profile.'''
        signup_form = UserCreationForm(self.request.POST)
        if signup_form.is_valid(): #check if the user creation form is valid
            user = signup_form.save()  #create the User object
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')  #log in the new user
            form.instance.user = user  #associate the User with the Profile
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
class FollowProfileView(ProfileRequiredMixin, TemplateView):
    '''View to follow a profile.'''
    template_name = 'mini_insta/show_profile.html'


    def dispatch(self, request, *args, **kwargs):
        '''Handle following the profile before rendering the template.'''
        user_profile = self.get_profile()
        profile_to_follow = Profile.objects.get(pk=kwargs['pk'])
        #create a Follow relationship if it doesn't already exist
        if user_profile != profile_to_follow:
            #check if already following
            existing_follow = Follow.objects.filter(
                follower_profile=user_profile,
                profile=profile_to_follow
            ).first()
            
            if not existing_follow:
                #create the follow relationship
                Follow.objects.create(
                    follower_profile=user_profile,
                    profile=profile_to_follow
                )
        return redirect('show_profile', pk=profile_to_follow.pk)
    
class DeleteFollowView(ProfileRequiredMixin, TemplateView):
    '''View to unfollow a profile.'''
    template_name = 'mini_insta/show_profile.html'

    def dispatch(self, request, *args, **kwargs):
        '''Handle unfollowing the profile before rendering the template.'''
        user_profile = self.get_profile()
        profile_to_unfollow = Profile.objects.get(pk=kwargs['pk'])
        
        #delete the Follow relationship if it exists
        Follow.objects.filter(
            follower_profile=user_profile,
            profile=profile_to_unfollow
        ).delete()
        
        return redirect('show_profile', pk=profile_to_unfollow.pk)
    
class LikePostView(ProfileRequiredMixin, TemplateView):
    '''View to like a post.'''
    template_name = 'mini_insta/show_post.html'

    def dispatch(self, request, *args, **kwargs):
        '''Handle liking the post before rendering the template.'''
        user_profile = self.get_profile()
        post_to_like = Post.objects.get(pk=kwargs['pk'])
        
        #create a Like relationship if it doesn't already exist
        if user_profile != post_to_like.profile:
            existing_like = Like.objects.filter(
                profile=user_profile,
                post=post_to_like
            ).first()
            
            if not existing_like:
                #create the like relationship
                Like.objects.create(
                    profile=user_profile,
                    post=post_to_like
                )
        return redirect('show_post', pk=post_to_like.pk)

class DeleteLikeView(ProfileRequiredMixin, TemplateView):
    '''View to unlike a post.'''
    template_name = 'mini_insta/show_post.html'

    def dispatch(self, request, *args, **kwargs):
        '''Handle unliking the post before rendering the template.'''
        user_profile = self.get_profile()
        post_to_unlike = Post.objects.get(pk=kwargs['pk'])
        
        #delete the Like relationship if it exists
        Like.objects.filter(
            profile=user_profile,
            post=post_to_unlike
        ).delete()
        
        return redirect('show_post', pk=post_to_unlike.pk)
    