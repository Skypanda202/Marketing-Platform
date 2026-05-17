from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["campaign", "recipient", "sender", "is_read"]
    search_fields = ["body", "sender__email", "recipient__email"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return Message.objects.select_related("sender", "recipient", "campaign")
        return Message.objects.select_related("sender", "recipient", "campaign").filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        Notification.objects.create(
            user=message.recipient,
            title="New message",
            body=f"{self.request.user.get_full_name() or self.request.user.email} sent you a message.",
            notification_type=Notification.Type.MESSAGE,
        )

    @action(detail=False, methods=["get"])
    def thread(self, request):
        other_user = request.query_params.get("user")
        qs = self.get_queryset()
        if other_user:
            qs = qs.filter(Q(sender_id=other_user) | Q(recipient_id=other_user))
        serializer = self.get_serializer(qs.order_by("created_at"), many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_read", "notification_type"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return Notification.objects.select_related("user")
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response(self.get_serializer(notification).data)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({"detail": "Notifications marked as read."})
