from rest_framework import routers
from .views import UserProfileViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('userprofile', UserProfileViewSet, basename='userprofile')  # Added basename parameter

urlpatterns = [
    path('', include(router.urls)),
]