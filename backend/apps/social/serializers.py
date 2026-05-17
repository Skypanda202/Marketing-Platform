from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Comment, FeedPost, Follow


class CommentSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source="author", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["id", "author", "created_at"]


class FeedPostSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source="author", read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    comment_count = serializers.IntegerField(source="comments.count", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = FeedPost
        fields = "__all__"
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and obj.likes.filter(id=request.user.id).exists())


class FollowSerializer(serializers.ModelSerializer):
    follower_detail = UserSerializer(source="follower", read_only=True)
    following_detail = UserSerializer(source="following", read_only=True)

    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["id", "follower", "created_at"]
