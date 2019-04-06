from rest_framework import serializers


class UserRepoSerializer(serializers.Serializer):
    fullName = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    cloneUrl = serializers.URLField(read_only=True)
    stars = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateTimeField(read_only=True)

