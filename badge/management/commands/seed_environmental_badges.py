from django.db import migrations
from django.core.management.base import BaseCommand
from badge.models import Badge  # Replace 'your_app_name' with your actual app name

class Command(BaseCommand):
    help = 'Seeds the database with environmental achievement badges'

    def handle(self, *args, **options):
        # Define environmental badges with increasing point thresholds
        badges = [
            {
                'name': 'Green Sprout',
                'description': 'You\'ve taken your first steps toward helping the environment. Keep going!',
                'points_threshold': 50
            },
            {
                'name': 'Eco Enthusiast',
                'description': 'Your environmental awareness is growing. You\'re making a difference!',
                'points_threshold': 150
            },
            {
                'name': 'Earth Guardian',
                'description': 'You\'ve shown consistent dedication to protecting our planet.',
                'points_threshold': 300
            },
            {
                'name': 'Conservation Champion',
                'description': 'Your environmental habits are making a significant impact. Very impressive!',
                'points_threshold': 500
            },
            {
                'name': 'Wilderness Protector',
                'description': 'Your commitment to preserving natural habitats is truly commendable.',
                'points_threshold': 750
            },
            {
                'name': 'Ocean Defender',
                'description': 'Your efforts are helping to keep our oceans clean and healthy.',
                'points_threshold': 1000
            },
            {
                'name': 'Climate Warrior',
                'description': 'You\'re actively fighting climate change through your daily choices.',
                'points_threshold': 1500
            },
            {
                'name': 'Sustainability Sage',
                'description': 'Your sustainable lifestyle choices are an inspiration to others.',
                'points_threshold': 2000
            },
            {
                'name': 'Ecosystem Engineer',
                'description': 'You\'re reshaping how humans interact with the environment in positive ways.',
                'points_threshold': 3000
            },
            {
                'name': 'Planet Savior',
                'description': 'You\'ve reached the highest level of environmental stewardship. The Earth thanks you!',
                'points_threshold': 5000
            },
        ]
        
        # Create badges in database
        badges_created = 0
        
        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults={
                    'description': badge_data['description'],
                    'points_threshold': badge_data['points_threshold']
                }
            )
            
            if created:
                badges_created += 1
                self.stdout.write(f"Created badge: {badge.name} (Points: {badge.points_threshold})")
            else:
                self.stdout.write(f"Badge already exists: {badge.name}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {badges_created} environmental badges!'))