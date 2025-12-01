## runtracker/serializers.py
## Author: Author: William Fugate wfugate@bu.edu
## description: serializers for runtracker app
from rest_framework import serializers
from .models import Run, UserProfile, Badge, Group, GroupMembership
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']



#serializer for Run model
class RunSerializer(serializers.ModelSerializer):
    '''Serializer for Run model'''
    user = UserSerializer(read_only=True) #serializer for user field

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source='user',
        write_only=True
    )
    class Meta:
        model = Run
        fields = ['id', 'user', 'user_id', 'distance_km', 'duration_seconds', 'center_lon', 'center_lat', 'start_time', 'route_data']
        read_only_fields = ['start_time']

class UserProfileSerializer(serializers.ModelSerializer):
    '''Serializer for UserProfile model'''
    user = UserSerializer(read_only=True) #serializer for user field

    def get_total_runs(self, obj):
        """Get total runs from UserProfile model method"""
        return obj.get_total_runs()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'total_distance_km', 'total_runs', 'best_distance_km']

class GroupSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_at', 'creator', 'is_creator', 'is_member']
    
    def get_is_creator(self, obj):
        """Check if current user is the creator"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.creator == request.user
        return False
    
    def get_is_member(self, obj):
        """Check if current user is a member"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user).exists()
        return False
    
class BadgeSerializer(serializers.ModelSerializer):
    '''Serializer for Badge model'''
    name = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    criteria_km = serializers.ReadOnlyField()
    
    class Meta:
        model = Badge
        fields = ['id', 'badge_type', 'name', 'description', 'criteria_km', 'earned_by']


class GroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer for GroupMembership model"""
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'group', 'joined_at']