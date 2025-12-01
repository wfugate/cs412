## runtracker/models.py
## Author: William Fugate wfugate@bu.edu
## description: model definitions for runtracker app
from django.db import models
from django.contrib.auth.models import User

class Run(models.Model):
    """Model to represent a single run"""
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user who did the run
    distance_km = models.FloatField() #distance covered in kilometers
    start_time = models.DateTimeField(auto_now_add=True) #when the run started
    duration_seconds = models.IntegerField(default=0) #duration of the run in seconds
    center_lat = models.FloatField() #geographic center latitude
    center_lon = models.FloatField() #geographic center longitude

    route_data = models.JSONField() #stores GPS route data as JSON list of coordinates

    class Meta:
        indexes = [
            models.Index(fields=['user', 'start_time']),
            models.Index(fields=['distance_km']),
        ]
        ordering = ['-start_time']

    def __str__(self):
        return f"Run by {self.user.username} on {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"
    

class UserProfile(models.Model):
    """Model to represent a user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE) #user associated with this profile
    total_distance_km = models.FloatField(default=0.0) #total distance of all runs in kilometers
    best_distance_km = models.FloatField(default=0.0)  #best single run distance in kilometers

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_total_runs(self):
        """Get the total number of runs from the Run model"""
        return self.user.run_set.count()


class Badge(models.Model):
    """Model to represent an achievement badge"""
    BADGE_TYPES = [
        ('1k', '1 Kilometer'), #types of achievable badges
        ('2k', '2 Kilometers'),
        ('5k', '5 Kilometers'),
        ('10k', '10 Kilometers'),
        ('20k', '20 Kilometers'),
        ('40k', '40 Kilometers'),
        ('100k', '100 Kilometers'),
    ]
    
    badge_type = models.CharField(max_length=10, choices=BADGE_TYPES, unique=True)
    earned_by = models.ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return f"{self.get_badge_type_display()} Badge"
    

    ##properties are attributes that we calculate automatically to avoid out of sync data
    @property #we can generate the criteria based on the badge type
    def criteria_km(self):
        """Get the distance criteria in km based on badge type"""
        return float(self.badge_type.replace('k', '')) #get rid of the k so we have just the number
    
    @property #we can find the name of the badge from the badge type
    def name(self): 
        """Get the name from badge type"""
        return f"{self.get_badge_type_display()} Runner"
    
    @property #we can also make a description from the badge type
    def description(self):
        """Auto-generate description from badge type"""
        distance = self.criteria_km
        if distance >= 100:
            return f"Run a total of {distance} kilometers"
        else:
            return f"Complete a single run of at least {distance} kilometers"


class Group(models.Model):
    """Model to represent a group of running partners"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owned_groups', null=True) #user who created the group

    def __str__(self):
        return self.name


class GroupMembership(models.Model):
    """Model to represent the many-to-many relationship between Users and Groups"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships') #user in the group
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships') #group the user belongs to
    joined_at = models.DateTimeField(auto_now_add=True) #when the user joined the group

    class Meta:
        unique_together = ('user', 'group')  #prevent duplicate memberships
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"