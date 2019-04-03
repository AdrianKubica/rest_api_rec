# from django.shortcuts import render
import datetime

from dataclasses import dataclass
from typing import NewType

from rest_framework import views
from rest_framework.response import Response
from core.serializers import UserRepoSerializer
from core.helpers import get_repo_data
from app.settings import GITHUB_URL

# NewType created for python type hints support
dt = NewType('dt', datetime.datetime)

@dataclass
class UserRepo:
    """Class provided to represent specified user repository details"""
    id: int
    fullName: str
    description: str
    cloneUrl: str
    stars: int
    createdAt: dt


user_repos = {
    1: UserRepo(id=1, fullName='Demo 1', description='xordoquy 1', cloneUrl='http://google.pl', stars=101, createdAt=datetime.datetime.now().isoformat()),
    2: UserRepo(id=2, fullName='Demo 2', description='xordoquy 2', cloneUrl='http://google.pl', stars=102, createdAt=datetime.datetime.now().isoformat()),
    3: UserRepo(id=3, fullName='Demo 3', description='xordoquy 3', cloneUrl='http://google.pl', stars=103, createdAt=datetime.datetime.now().isoformat()),
}

class UserRepoView(views.APIView):
    serializer_class = UserRepoSerializer

    def get(self, request, owner, repo, format=None):
        repo_data = get_repo_data(GITHUB_URL, owner, repo)
        serializer = UserRepoSerializer(repo_data)
        return Response(serializer.data)