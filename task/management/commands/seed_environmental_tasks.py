from django.db import migrations
from django.core.management.base import BaseCommand
from task.models import Task  # Replace 'your_app_name' with your actual app name

class Command(BaseCommand):
    help = 'Seeds the database with environmental tasks'

    def handle(self, *args, **options):
        # Delete existing tasks to avoid duplicates (optional)
        # Task.objects.all().delete()
        
        # Define environmental tasks
        daily_tasks = [
            {
                'name': 'Reusable Water Bottle',
                'description': 'Use a reusable water bottle instead of buying plastic bottles.',
                'points': 5,
                'task_type': 'daily'
            },
            {
                'name': 'Electronics Power Off',
                'description': 'Turn off all electronics when not in use to conserve energy.',
                'points': 3,
                'task_type': 'daily'
            },
            {
                'name': 'Shorter Shower',
                'description': 'Take a shorter shower to conserve water.',
                'points': 4,
                'task_type': 'daily'
            },
            {
                'name': 'Vegetarian Meal',
                'description': 'Choose a vegetarian meal option to reduce carbon footprint.',
                'points': 6,
                'task_type': 'daily'
            },
            {
                'name': 'Public Transport',
                'description': 'Use public transportation, bike, or walk instead of driving.',
                'points': 7,
                'task_type': 'daily'
            },
            {
                'name': 'Lights Off',
                'description': 'Turn off lights when leaving rooms to save electricity.',
                'points': 2,
                'task_type': 'daily'
            },
            {
                'name': 'Reusable Bag',
                'description': 'Use a reusable bag for shopping instead of plastic bags.',
                'points': 4,
                'task_type': 'daily'
            },
        ]
        
        weekly_tasks = [
            {
                'name': 'E-waste Recycling',
                'description': 'Properly recycle electronic waste at a designated collection point.',
                'points': 15,
                'task_type': 'weekly'
            },
            {
                'name': 'Plant Care',
                'description': 'Take care of a houseplant or garden to improve air quality and biodiversity.',
                'points': 10,
                'task_type': 'weekly'
            },
            {
                'name': 'Energy Audit',
                'description': 'Conduct a simple energy audit of your home to identify ways to reduce consumption.',
                'points': 12,
                'task_type': 'weekly'
            },
            {
                'name': 'Beach/Park Cleanup',
                'description': 'Participate in a local cleanup event or spend 30 minutes collecting trash in a public space.',
                'points': 20,
                'task_type': 'weekly'
            },
            {
                'name': 'Meatless Week',
                'description': 'Go an entire week without consuming meat products.',
                'points': 25,
                'task_type': 'weekly'
            },
            {
                'name': 'Green Shopping',
                'description': 'Purchase products with eco-friendly packaging or from sustainable brands.',
                'points': 15,
                'task_type': 'weekly'
            },
            {
                'name': 'Water Conservation Check',
                'description': 'Check for and fix any water leaks in your home.',
                'points': 18,
                'task_type': 'weekly'
            },
        ]
        
        # Create tasks in database
        tasks_created = 0
        
        for task_data in daily_tasks + weekly_tasks:
            task, created = Task.objects.get_or_create(
                name=task_data['name'],
                defaults={
                    'description': task_data['description'],
                    'points': task_data['points'],
                    'task_type': task_data['task_type']
                }
            )
            
            if created:
                tasks_created += 1
                self.stdout.write(f"Created task: {task.name}")
            else:
                self.stdout.write(f"Task already exists: {task.name}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {tasks_created} environmental tasks!'))