from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from userTask.models import UserTask
from userTask.serializers import UserTaskSerializer
from userTask.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from UserProfile.models import UserProfile
from badge.models import Badge
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta


class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return UserTask.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def today(self, request):
        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        
        user_tasks = UserTask.objects.filter(
            user=request.user,
            completed_at__gte=today,
            completed_at__lt=tomorrow
        )
        
        serializer = self.get_serializer(user_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def uncomplete_task(self, request, pk=None):
        user_task = self.get_object()
        
        # Ensure the task belongs to the current user
        if user_task.user != request.user:
            return Response({
                'message': 'You do not have permission to modify this task'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Remove points from user profile
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.total_points -= user_task.task.points
            profile.save()
            
            # Remove badges if points drop below threshold
            badges_to_remove = Badge.objects.filter(
                points_threshold__gt=profile.total_points
            ).intersection(profile.badges.all())
            profile.badges.remove(*badges_to_remove)
        except UserProfile.DoesNotExist:
            # Handle case where profile doesn't exist
            pass
        
        # Delete the user task
        # user_task.delete()
        
        return Response({
            'task_uncompleted': True,
            'points_deducted': user_task.task.points
        }, status=status.HTTP_200_OK)
