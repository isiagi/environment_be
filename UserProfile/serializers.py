from rest_framework import serializers
from .models import UserProfile
from badge.serializers import BadgeSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    badges = BadgeSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['total_points', 'badges']