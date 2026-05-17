from django.contrib import admin

from .models import Comment, FeedPost, Follow


@admin.register(FeedPost)
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ("author", "campaign", "visibility", "created_at")
    list_filter = ("visibility", "created_at")
    search_fields = ("caption", "author__email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("body", "author__email")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
