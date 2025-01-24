from django.db import models
from users.models import CustomUser as User
from badge.models import Badge

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge)
    
    def __str__(self):
        return self.user.username