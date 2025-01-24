from django.db import models
from task.models import Task
from users.models import CustomUser as User

# Create your models here.
class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'task', 'completed_at')
