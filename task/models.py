from django.db import models

# Create your models here.
class Task(models.Model):
    TASK_TYPES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    task_type = models.CharField(max_length=10, choices=TASK_TYPES)
    
    def __str__(self):
        return self.name
