from rest_framework import routers
from .views import TaskViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('task', TaskViewSet, basename='task')  # Added basename parameter

urlpatterns = [
    path('', include(router.urls)),
]