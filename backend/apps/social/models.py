from django.conf import settings
from django.db import models


class FeedPost(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "PUBLIC", "Public"
        CONNECTIONS = "CONNECTIONS", "Connections"
        PRIVATE = "PRIVATE", "Private"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_posts")
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, null=True, blank=True, related_name="feed_posts")
    caption = models.TextField()
    media = models.FileField(upload_to="feed/", blank=True, null=True)
    external_media_url = models.URLField(blank=True)
    hashtags = models.JSONField(default=list, blank=True)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["author", "created_at"]), models.Index(fields=["visibility", "created_at"])]

    def __str__(self):
        return f"{self.author.email}: {self.caption[:40]}"


class Comment(models.Model):
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feed_comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        indexes = [models.Index(fields=["follower", "following"])]
