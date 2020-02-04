from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import action


class VotingMixin(object):

    @staticmethod
    def vote_helper(pk, request, vote_type):
        content_obj = Votable.get_object(pk)
        user = request.user
        content_obj.toggle_vote(user, vote_type)

        if isinstance(content_obj, Comment):
            Serializer = CommentSerializer
        else:
            Serializer = PostSerializer

        serializer = Serializer(content_obj, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_name='upvote', url_path='upvote',
                  permission_classes=[permissions.IsAuthenticated])
    def upvote(self, request, pk=None):
        return VotingMixin.vote_helper(pk, request, UserVote.UP_VOTE)

    @action(methods=['post'], detail=True, url_name='downvote', url_path='downvote',
                  permission_classes=[permissions.IsAuthenticated])
    def downvote(self, request, pk=None):
        return VotingMixin.vote_helper(pk, request, UserVote.DOWN_VOTE)