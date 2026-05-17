from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Message, Notification


class MessageSerializer(serializers.ModelSerializer):
    sender_detail = UserSerializer(source="sender", read_only=True)
    recipient_detail = UserSerializer(source="recipient", read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "sender", "is_read", "created_at"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["id", "user", "created_at"]
