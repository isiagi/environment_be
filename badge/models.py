from django.db import models

# Create your models here.
class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_threshold = models.IntegerField()
    
    def __str__(self):
        return self.name