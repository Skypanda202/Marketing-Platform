from django.conf import settings
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    body = models.TextField()
    attachment = models.FileField(upload_to="message_attachments/", blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["sender", "recipient", "created_at"])]

    def __str__(self):
        return f"{self.sender} -> {self.recipient}"


class Notification(models.Model):
    class Type(models.TextChoices):
        INVITATION = "INVITATION", "Invitation"
        MESSAGE = "MESSAGE", "Message"
        PAYMENT = "PAYMENT", "Payment"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    notification_type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
