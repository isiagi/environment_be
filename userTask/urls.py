from rest_framework import routers
from .views import UserTaskViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('user-tasks', UserTaskViewSet, basename='usertask')  # Added basename parameter

urlpatterns = [
    path('', include(router.urls)),
]