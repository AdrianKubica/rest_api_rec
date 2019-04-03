import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

# from core.views import UserRepo
import datetime
from dataclasses import dataclass
from typing import NewType

# NewType created for python type hints support
dt = NewType('dt', datetime.datetime)

@dataclass
class UserRepo:
    """Class provided to represent specified user repository details"""
    fullName: str
    description: str
    cloneUrl: str
    stars: int
    createdAt: dt

class UserRepoSerializer(serializers.Serializer):
    """Serializer for UserRepo class"""
    # id = serializers.IntegerField(read_only=True)
    fullName = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    cloneUrl = serializers.URLField(read_only=True)
    stars = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return UserRepo(**validated_data)

    # def get_createdAt(self, obj):
    #     date = datetime.datetime.fromtimestamp(obj['createdAt'])
    #     return date.isoformat()
