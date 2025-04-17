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
from datetime import datetime, timedelta

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_tasks_with_status(self, request):
        """
        Get tasks with their completion status for the current period (daily or weekly).
        Returns all tasks of the requested type with a is_completed flag.
        """
        task_type = request.query_params.get('task_type', 'daily')
        user = request.user
        
        # Validate task type
        if task_type not in dict(Task.TASK_TYPES):
            return Response({
                'message': f"Invalid task type. Choose from: {', '.join(dict(Task.TASK_TYPES).keys())}"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get all tasks of the specified type
        tasks = Task.objects.filter(task_type=task_type)
        
        # Define the time threshold based on task type
        if task_type == 'daily':
            # Start of current day
            today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            time_threshold = today
        else:
            # Start of current week (assuming Monday is the first day of the week)
            today = timezone.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Monday
            time_threshold = timezone.make_aware(datetime.combine(start_of_week, datetime.min.time()))
        
        # Prepare response with tasks and their completion status
        response_data = []
        for task in tasks:
            # Check if task was completed in the current period
            completed_in_period = UserTask.objects.filter(
                user=user,
                task=task,
                completed_at__gte=time_threshold,
                is_completed=True
            ).exists()
            
            # Serialize the task and add completion status
            task_data = self.get_serializer(task).data
            task_data['is_completed'] = completed_in_period
            response_data.append(task_data)
        
        return Response(response_data, status=status.HTTP_200_OK)

    
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def uncomplete_task(self, request, pk=None):
        task = self.get_object()
        user = request.user

        # Find the most recent completed task
        try:
            user_task = UserTask.objects.filter(
                user=user,
                task=task,
                is_completed=True
            ).latest('completed_at')
        except UserTask.DoesNotExist:
            return Response({
                'message': 'No completed task found'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update user points
        profile = UserProfile.objects.get(user=user)
        profile.total_points -= task.points
        profile.save()

        # Delete the user task
        user_task.delete()

        # Re-check badges after point reduction
        self._check_and_award_badges(profile)

        return Response({
            'task_uncompleted': True,
            'points_deducted': task.points,
            'total_points': profile.total_points
        }, status=status.HTTP_200_OK)
    
    def _check_and_award_badges(self, profile):
        # Award badges based on points
        badges_to_award = Badge.objects.filter(
            points_threshold__lte=profile.total_points
        ).exclude(id__in=profile.badges.all())
        
        profile.badges.add(*badges_to_award)
