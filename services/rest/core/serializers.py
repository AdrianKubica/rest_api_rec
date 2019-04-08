"""
Serializers module is responsible for data serialization

"""

from rest_framework import serializers


class UserRepoSerializer(serializers.Serializer):
    """
    UserRepoSerializer is responsible for preparation of serialized version data object
    """
    fullName: str = serializers.CharField(read_only=True)
    description: str = serializers.CharField(read_only=True)
    cloneUrl: str = serializers.URLField(read_only=True)
    stars: int = serializers.IntegerField(read_only=True)
    # According to Github API repository all timestamps are returned in ISO 8601 date format.
    # Keep in mind that this API also sets HTTP header for each request {'Accept': 'application/vnd.github.v3+json'}
    # to protect for changing Github API versions which may results also with change date format
    createdAt: str = serializers.DateTimeField(read_only=True)
