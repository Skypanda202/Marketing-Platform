from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Comment, FeedPost, Follow
from .serializers import CommentSerializer, FeedPostSerializer, FollowSerializer


class FeedPostViewSet(viewsets.ModelViewSet):
    serializer_class = FeedPostSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["author", "campaign", "visibility"]
    search_fields = ["caption", "hashtags", "author__email", "author__username"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        qs = FeedPost.objects.select_related("author", "campaign").prefetch_related("likes", "comments")
        if user.role == "ADMIN":
            return qs
        following_ids = Follow.objects.filter(follower=user).values_list("following_id", flat=True)
        return qs.filter(Q(visibility="PUBLIC") | Q(author=user) | Q(author_id__in=following_ids)).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        return Response(self.get_serializer(post).data)

    @action(detail=True, methods=["post"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response(self.get_serializer(post).data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["post", "author"]

    def get_queryset(self):
        qs = Comment.objects.select_related("post", "author", "post__author")
        if self.request.user.role == "ADMIN":
            return qs
        following_ids = Follow.objects.filter(follower=self.request.user).values_list("following_id", flat=True)
        return qs.filter(Q(post__visibility="PUBLIC") | Q(post__author=self.request.user) | Q(post__author_id__in=following_ids)).distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["following", "follower"]

    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return Follow.objects.select_related("follower", "following")
        return Follow.objects.select_related("follower", "following").filter(Q(follower=self.request.user) | Q(following=self.request.user))

    def perform_create(self, serializer):
        if serializer.validated_data["following"] == self.request.user:
            raise ValidationError("You cannot follow yourself.")
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=["post"])
    def unfollow(self, request):
        following_id = request.data.get("following")
        deleted, _ = Follow.objects.filter(follower=request.user, following_id=following_id).delete()
        return Response({"deleted": deleted}, status=status.HTTP_200_OK)
