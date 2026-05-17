import secrets

from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import AdCampaignLaunch, AdPlatformConnection
from .serializers import AdCampaignLaunchSerializer, AdPlatformConnectionSerializer
from .services import GoogleAdsService, MetaAdsService


class AdPlatformConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = AdPlatformConnectionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["provider", "is_active"]
    search_fields = ["account_id", "account_name"]

    def get_queryset(self):
        qs = AdPlatformConnection.objects.select_related("owner")
        if self.request.user.role == "ADMIN":
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AdCampaignLaunchViewSet(viewsets.ModelViewSet):
    serializer_class = AdCampaignLaunchSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["connection", "campaign", "status", "dry_run"]

    def get_queryset(self):
        qs = AdCampaignLaunch.objects.select_related("campaign", "connection", "connection__owner")
        if self.request.user.role == "ADMIN":
            return qs
        return qs.filter(connection__owner=self.request.user)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        launch = self.get_object()
        try:
            if launch.connection.provider == AdPlatformConnection.Provider.META:
                payload = MetaAdsService.create_paused_campaign(launch.connection, launch)
            else:
                payload = GoogleAdsService.create_paused_campaign(launch.connection, launch)
            launch.platform_response = payload
            launch.platform_campaign_id = payload.get("id", "")
            launch.status = AdCampaignLaunch.Status.SUBMITTED if not launch.dry_run else AdCampaignLaunch.Status.VALIDATED
            launch.save(update_fields=["platform_response", "platform_campaign_id", "status", "updated_at"])
            return Response(self.get_serializer(launch).data)
        except Exception as exc:
            launch.status = AdCampaignLaunch.Status.FAILED
            launch.platform_response = {"error": str(exc)}
            launch.save(update_fields=["status", "platform_response", "updated_at"])
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="meta/start")
    def meta_start(self, request):
        return Response({"authorization_url": MetaAdsService.auth_url(secrets.token_urlsafe(24))})

    @action(detail=False, methods=["get"], url_path="google/start")
    def google_start(self, request):
        return Response({"authorization_url": GoogleAdsService.auth_url(secrets.token_urlsafe(24))})

    @action(detail=False, methods=["get"], url_path="meta/callback", permission_classes=[])
    def meta_callback(self, request):
        code = request.query_params.get("code")
        if code and settings.META_APP_SECRET:
            token_payload = MetaAdsService.exchange_code(code)
            return redirect(f"{settings.FRONTEND_URL}/integrations?provider=meta&connected=1&token_preview={token_payload.get('access_token', '')[:8]}")
        return redirect(f"{settings.FRONTEND_URL}/integrations?provider=meta&connected=0")

    @action(detail=False, methods=["get"], url_path="google/callback", permission_classes=[])
    def google_callback(self, request):
        code = request.query_params.get("code")
        if code and settings.GOOGLE_CLIENT_SECRET:
            token_payload = GoogleAdsService.exchange_code(code)
            return redirect(f"{settings.FRONTEND_URL}/integrations?provider=google&connected=1&token_preview={token_payload.get('access_token', '')[:8]}")
        return redirect(f"{settings.FRONTEND_URL}/integrations?provider=google&connected=0")
