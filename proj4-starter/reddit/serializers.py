from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers

# "eid": "97f56643-36f6-4330-810b-a974c589ef07"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class BaseSerializer(serializers.ModelSerializer):
    eid = serializers.UUIDField(read_only=True)

    def update(self, instance, validated_data):
        if hasattr(self, 'protected_update_fields'):
            for protected_field in self.protected_update_fields:
                if protected_field in validated_data:
                    raise serializers.ValidationError({
                        protected_field: 'You cannot change this field.',
                    })

        return super().update(instance, validated_data)

class ContentSerializer(BaseSerializer):
    user_vote = serializers.SerializerMethodField()

    def get_user_vote(self, obj):
        return obj.get_user_vote(self.context['request'].user)

class SubRedditSerializer(BaseSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    moderators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=True, read_only=False)

    protected_update_fields = ['moderators']

    class Meta:
        model = SubReddit
        fields = ('eid', 'name', 'cover_image_url', 'posts', 'moderators')

    def validate_moderators(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('Need to include at least one moderator!')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        moderators = validated_data.pop('moderators')

        if user not in moderators: moderators.append(user)

        subreddit = SubReddit.objects.create(**validated_data)
        for mod in moderators: subreddit.moderators.add(mod)

        return subreddit


class PostSerializer(ContentSerializer):
    submitter = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    children = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    subreddits = serializers.PrimaryKeyRelatedField(many=True, queryset=SubReddit.objects.all(), required=True)

    protected_update_fields = ['subreddits']

    class Meta:
        model = Post
        fields = ('eid', 'title', 'submitter', 'text', 'children', 'subreddits', 'comment_count', 'upvote_count', 'downvote_count', 'user_vote')
        read_only_fields = ('comment_count', 'upvote_count', 'downvote_count')

    def validate_subreddits(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('Need to include at least one subreddit to post to!')
        return value

    def create(self, validated_data):
        subreddits = validated_data.pop('subreddits')
        validated_data['submitter'] = self.context['request'].user
        post = Post.objects.create(**validated_data)
        for subreddit in subreddits:
            SubRedditPost.objects.create(subreddit=subreddit, post=post)
        return post


class CommentSerializer(ContentSerializer):
    author = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    children = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=True, read_only=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, read_only=False,
                                                allow_null=True)

    class Meta:
        model = Comment
        fields = ('eid', 'post', 'author', 'text', 'parent', 'children', 'upvote_count', 'downvote_count', 'user_vote')
        read_only_fields = ('upvote_count', 'downvote_count')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        comment = Comment.objects.create(**validated_data)
        return comment