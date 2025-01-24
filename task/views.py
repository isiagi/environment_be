from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from userTask.models import UserTask
from UserProfile.models import UserProfile
from badge.models import Badge
from task.serializers import TaskSerializer
from .permissions import IsAuthenticated
from userTask.permissions import IsOwnerOrReadOnly

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete_task(self, request, pk=None):
        task = self.get_object()
        user = request.user
        
        # Check for recent task completion
        time_threshold = (
            timezone.now() - timedelta(days=1) 
            if task.task_type == 'daily' 
            else timezone.now() - timedelta(weeks=1)
        )
        
        recent_completion = UserTask.objects.filter(
            user=user, 
            task=task, 
            completed_at__gte=time_threshold,
            is_completed=True
        ).exists()
        
        if recent_completion:
            return Response({
                'message': 'Task already completed recently'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user task
        user_task = UserTask.objects.create(
            user=user, 
            task=task, 
            is_completed=True
        )
        
        # Update user points
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.total_points += task.points
        profile.save()
        
        # Check and award badges
        self._check_and_award_badges(profile)
        
        return Response({
            'task_completed': True,
            'points_awarded': task.points,
            'total_points': profile.total_points
        }, status=status.HTTP_200_OK)
    
    def _check_and_award_badges(self, profile):
        # Award badges based on points
        badges_to_award = Badge.objects.filter(
            points_threshold__lte=profile.total_points
        ).exclude(id__in=profile.badges.all())
        
        profile.badges.add(*badges_to_award)
