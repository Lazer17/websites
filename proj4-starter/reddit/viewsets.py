from .models import *
from .serializers import *

from django.db.models import Q
from django.contrib.auth.models import User
from .mixins import VotingMixin
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .permissions import IsModeratorOrReadOnly, IsSubmitterOrReadOnly


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class SubRedditViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    """
    API endpoint that allows SubReddits to be viewed or edited.
    """
    queryset = SubReddit.objects.all()
    serializer_class = SubRedditSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly)

class PostViewSet(viewsets.ModelViewSet, VotingMixin):
    """
    API endpoint that allows Posts to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsSubmitterOrReadOnly)

class CommentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, VotingMixin):
    """
    API endpoint that allows Comments to be viewed.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)