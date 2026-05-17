from django.db.models import Count
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsBrandRole
from apps.ai_engine.services import ROIPredictionService
from apps.communications.models import Notification

from .models import Campaign, CampaignInvitation
from .serializers import CampaignInvitationSerializer, CampaignSerializer


class CampaignViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "niche", "brand"]
    search_fields = ["title", "description", "goals", "niche"]
    ordering_fields = ["budget", "start_date", "end_date", "created_at"]

    def get_queryset(self):
        qs = Campaign.objects.select_related("brand", "brand__user").annotate(invitation_count=Count("invitations"))
        user = self.request.user
        if user.role == "ADMIN":
            return qs
        if user.role == "BRAND":
            return qs.filter(brand__user=user)
        return qs.filter(invitations__influencer__user=user).distinct()

    def perform_create(self, serializer):
        campaign = serializer.save(brand=self.request.user.brand_profile)
        campaign.expected_roi = ROIPredictionService.predict_campaign_roi(campaign)
        campaign.save(update_fields=["expected_roi"])

    @action(detail=True, methods=["post"], permission_classes=[IsBrandRole])
    def predict_roi(self, request, pk=None):
        campaign = self.get_object()
        return Response({"campaign": campaign.id, "predicted_roi": ROIPredictionService.predict_campaign_roi(campaign)})


class CampaignInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = CampaignInvitationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "campaign", "influencer"]
    search_fields = ["message", "campaign__title", "influencer__display_name"]
    ordering_fields = ["created_at", "proposed_rate"]

    def get_queryset(self):
        qs = CampaignInvitation.objects.select_related("campaign", "campaign__brand", "influencer", "influencer__user", "invited_by")
        user = self.request.user
        if user.role == "ADMIN":
            return qs
        if user.role == "BRAND":
            return qs.filter(campaign__brand__user=user)
        return qs.filter(influencer__user=user)

    def perform_create(self, serializer):
        invitation = serializer.save(invited_by=self.request.user)
        Notification.objects.create(
            user=invitation.influencer.user,
            title="New campaign invitation",
            body=f"{invitation.campaign.brand.company_name} invited you to {invitation.campaign.title}.",
            notification_type=Notification.Type.INVITATION,
        )

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.influencer.user != request.user:
            return Response({"detail": "Only the invited influencer can accept."}, status=status.HTTP_403_FORBIDDEN)
        invitation.status = CampaignInvitation.Status.ACCEPTED
        invitation.responded_at = timezone.now()
        invitation.save(update_fields=["status", "responded_at", "updated_at"])
        return Response(self.get_serializer(invitation).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        invitation = self.get_object()
        if invitation.influencer.user != request.user:
            return Response({"detail": "Only the invited influencer can reject."}, status=status.HTTP_403_FORBIDDEN)
        invitation.status = CampaignInvitation.Status.REJECTED
        invitation.responded_at = timezone.now()
        invitation.save(update_fields=["status", "responded_at", "updated_at"])
        return Response(self.get_serializer(invitation).data)

    @action(detail=True, methods=["post"])
    def submit_content(self, request, pk=None):
        invitation = self.get_object()
        if invitation.influencer.user != request.user:
            return Response({"detail": "Only the invited influencer can submit content."}, status=status.HTTP_403_FORBIDDEN)
        invitation.submitted_content_url = request.data.get("submitted_content_url", "")
        invitation.submitted_content_notes = request.data.get("submitted_content_notes", "")
        invitation.save(update_fields=["submitted_content_url", "submitted_content_notes", "updated_at"])
        return Response(self.get_serializer(invitation).data)
