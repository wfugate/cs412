## tracker/views.py
## Author: William Fugate wfugate@bu.edu
## description: views file for run tracker app
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Run, UserProfile, Group, GroupMembership, User, Badge
from .serializers import RunSerializer, UserProfileSerializer, GroupSerializer, BadgeSerializer, GroupMembershipSerializer, UserSerializer

PROXIMITY_THRESHOLD_METERS = 500


class UserListAPIView(generics.ListAPIView):
    """List all users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RunListCreateAPIView(generics.ListCreateAPIView):
    """An API view to return a listing of Runs or create a new Run."""
    serializer_class = RunSerializer
    
    def get_queryset(self):
        """Filter runs to only show the authenticated user's runs"""
        if self.request.user.is_authenticated:
            runs = Run.objects.filter(user=self.request.user)
            return runs
        return Run.objects.none()
    
    def perform_create(self, serializer):
        """Override to update user profile stats when a new run is created."""
        new_run = serializer.save(user=self.request.user)
        
        try:
            with transaction.atomic():
                profile = UserProfile.objects.select_for_update().get(user=new_run.user)
                profile.total_distance_km += new_run.distance_km
                if new_run.distance_km > profile.best_distance_km:
                    profile.best_distance_km = new_run.distance_km
                profile.save()
                for badge in Badge.objects.all():
                    #single run badges (< 100k)
                    if badge.criteria_km < 100:
                        if new_run.distance_km >= badge.criteria_km:
                            badge.earned_by.add(new_run.user)
                    #total distance badges (>= 100k)
                    else:
                        if profile.total_distance_km >= badge.criteria_km:
                            badge.earned_by.add(new_run.user)
        except UserProfile.DoesNotExist:
            pass

class RunDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """An API view to retrieve, update, or delete a Run."""
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    """An API view to retrieve a user's Profile stats."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__id'


class RunProximitySearchAPIView(APIView):
    """An API view to find runs within proximity of a target run's center."""

    def get(self, request, run_id):
        """Finds runs whose geographic center is within the specified distance of the target run's center."""
        try:
            target_run = Run.objects.get(pk=run_id)
        except Run.DoesNotExist:
            return Response(
                {"error": "Run not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        target_center = (target_run.center_lat, target_run.center_lon)
        
        #get all other runs to compare
        candidate_runs = Run.objects.exclude(pk=run_id).select_related('user')
        nearby_runs_data = []

        #compare
        for candidate in candidate_runs:
            candidate_center = (candidate.center_lat, candidate.center_lon)
            
            #calculate distance between centers
            distance = geodesic(target_center, candidate_center).meters
            
            if distance <= PROXIMITY_THRESHOLD_METERS: #configurable currently 500 meters
                nearby_runs_data.append({
                    "id": candidate.id,
                    "user": candidate.user.username,
                    "distance_from_center_m": round(distance, 2),
                    "run_distance": candidate.distance_km,
                    "run_time": candidate.duration_seconds,
                })

        return Response(nearby_runs_data)
    

class GroupRemoveMemberAPIView(APIView):
    """Remove a member from a group"""
    
    def delete(self, request, group_id, user_id):
        group = get_object_or_404(Group, pk=group_id)
        
        if group.creator != request.user: #check if the requester is the creator
            return Response(
                {"error": "Only the group creator can remove members"},
                status=status.HTTP_403_FORBIDDEN
            )

        membership = GroupMembership.objects.filter(group=group, user_id=user_id).first() #find the membership we're removing
        
        if membership:
            membership.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response( #otherwise not found
            {"error": "User is not a member of this group"},
            status=status.HTTP_404_NOT_FOUND
        )


class GroupAddMemberAPIView(APIView):
    """Add a member to a group (ANYONE HAS PERMISSION)"""
    
    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id) #get the group

        is_member = GroupMembership.objects.filter(group=group, user=request.user).exists() #check if requester is a member
        
        if not is_member: #if theyre not a member they cant invite others
            return Response(
                {"error": "only group members can invite others!"},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get('user_id') #get the user to add
        user = get_object_or_404(User, pk=user_id) #get the user object
        
        membership, created = GroupMembership.objects.get_or_create(group=group, user=user) #create the membership if it doesnt exist
        
        if created:
            return Response(
                {"message": "Member added successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "User is already a member"},
                status=status.HTTP_200_OK
            )
    
class GroupListCreateAPIView(generics.ListCreateAPIView):
    """View to list all groups or create a new group"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_serializer_context(self):
        """Pass the request to the serializer context"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        """Set the creator to the logged in user"""
        group = serializer.save(creator=self.request.user)
        #add the creator as a member too
        GroupMembership.objects.create(group=group, user=self.request.user)

class GroupDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a group"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        
        if group.creator != request.user:
            return Response(
                {"error": "Only the group creator can delete this group"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)

class BadgeListAPIView(generics.ListAPIView):
    """View to list all badges"""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class BadgeDetailAPIView(generics.RetrieveAPIView):
    """View to retrieve a badge"""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class GroupMembersListAPIView(generics.ListAPIView):
    """View to list all members of a group"""
    serializer_class = GroupMembershipSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return GroupMembership.objects.filter(group=group_id)
