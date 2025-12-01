## runtracker/management/commands/populate_data.py
## Run with: python manage.py populate_data

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from runtracker.models import Run, UserProfile, Badge, Group, GroupMembership
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data population...')
        
        # Get existing users or create some
        users = list(User.objects.all())
        if len(users) < 3:
            self.stdout.write('Creating sample users...')
            for i in range(3):
                user, created = User.objects.get_or_create(
                    username=f'runner{i+1}',
                    defaults={'email': f'runner{i+1}@example.com'}
                )
                if created:
                    user.set_password('password123')
                    user.save()
                users.append(user)
        
        # Create UserProfiles for all users
        self.stdout.write('Creating user profiles...')
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f'  Created profile for {user.username}')
        
        # Create Runs
        self.stdout.write('Creating runs...')
        # Boston area coordinates (around BU campus)
        base_lat = 42.3505
        base_lon = -71.1054
        
        for user in users[:3]:  # Create runs for first 3 users
            num_runs = random.randint(3, 5)
            for i in range(num_runs):
                # Random location within ~1km of base
                center_lat = base_lat + random.uniform(-0.01, 0.01)
                center_lon = base_lon + random.uniform(-0.01, 0.01)
                
                # Generate a simple route (5-10 points around the center)
                route_points = []
                num_points = random.randint(5, 10)
                for j in range(num_points):
                    route_points.append({
                        'latitude': center_lat + random.uniform(-0.005, 0.005),
                        'longitude': center_lon + random.uniform(-0.005, 0.005),
                        'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
                    })
                
                distance = round(random.uniform(2.0, 15.0), 2)  # 2-15 km
                duration = int(distance * random.randint(300, 450))  # ~5-7.5 min/km
                
                run = Run.objects.create(
                    user=user,
                    distance_km=distance,
                    duration_seconds=duration,
                    center_lat=center_lat,
                    center_lon=center_lon,
                    route_data=route_points
                )
                
                # Update profile stats
                profile = user.userprofile
                profile.total_distance_km += distance
                if distance > profile.best_distance_km:
                    profile.best_distance_km = distance
                profile.save()
                
                self.stdout.write(f'  Created run for {user.username}: {distance}km')
        
        # Create Badges
        self.stdout.write('Creating badges...')
        badge_types = ['1k', '2k', '5k', '10k', '20k', '40k', '100k']

        for badge_type in badge_types:
            badge, created = Badge.objects.get_or_create(badge_type=badge_type)
            
            # Award badges to users who meet criteria
            for user in users:
                profile = user.userprofile
                runs = Run.objects.filter(user=user)
                criteria = badge.criteria_km
                
                # Single run distance badges (< 100k)
                if criteria < 100:
                    if runs.filter(distance_km__gte=criteria).exists():
                        badge.earned_by.add(user)
                # Total distance badges (>= 100k)
                else:
                    if profile.total_distance_km >= criteria:
                        badge.earned_by.add(user)
            
            if created:
                self.stdout.write(f'  Created badge: {badge.name}')
                
        # Create Groups
        self.stdout.write('Creating groups...')
        group_data = [
            {'name': 'BU Morning Runners', 'description': 'Early morning running group for BU students'},
            {'name': 'Charles River Crew', 'description': 'Running along the Charles River path'},
            {'name': 'Weekend Warriors', 'description': 'Casual weekend running group'},
            {'name': 'Marathon Training Squad', 'description': 'Training for upcoming marathons'},
        ]
        
        for i, data in enumerate(group_data[:random.randint(3, 4)]):
            creator = users[i % len(users)]
            group, created = Group.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'creator': creator
                }
            )
            
            if created:
                # Add creator as member
                GroupMembership.objects.create(group=group, user=creator)
                
                # Add 2-3 random other members
                other_users = [u for u in users if u != creator]
                num_members = random.randint(2, min(3, len(other_users)))
                for member in random.sample(other_users, num_members):
                    GroupMembership.objects.create(group=group, user=member)
                
                member_count = group.memberships.count()
                self.stdout.write(f'  Created group: {group.name} ({member_count} members)')
        
        self.stdout.write(self.style.SUCCESS('Database population complete!'))
        self.stdout.write(f'Summary:')
        self.stdout.write(f'  Users: {User.objects.count()}')
        self.stdout.write(f'  Runs: {Run.objects.count()}')
        self.stdout.write(f'  Badges: {Badge.objects.count()}')
        self.stdout.write(f'  Groups: {Group.objects.count()}')
        self.stdout.write(f'  Group Memberships: {GroupMembership.objects.count()}')