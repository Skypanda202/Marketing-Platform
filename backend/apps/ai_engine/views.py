from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import InfluencerProfile
from apps.accounts.serializers import InfluencerProfileSerializer
from apps.campaigns.models import Campaign

from .services import FakeEngagementService, RecommendationService, ROIPredictionService, SentimentService


class EmptySerializer(serializers.Serializer):
    pass


class AIViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    @action(detail=False, methods=["get"])
    def recommendations(self, request):
        queryset = InfluencerProfile.objects.select_related("user").all()
        ranked = RecommendationService.rank_influencers(queryset, request.user)
        return Response(InfluencerProfileSerializer(ranked[:10], many=True).data)

    @action(detail=False, methods=["post"])
    def sentiment(self, request):
        return Response(SentimentService.analyze(request.data.get("text", "")))

    @action(detail=False, methods=["post"])
    def fake_engagement(self, request):
        score = FakeEngagementService.score(
            followers=int(request.data.get("followers", 0)),
            engagement_rate=float(request.data.get("engagement_rate", 0)),
            recent_likes=request.data.get("recent_likes", []),
            recent_comments=request.data.get("recent_comments", []),
        )
        return Response({"fake_follower_score": score, "risk": "high" if score >= 65 else "medium" if score >= 35 else "low"})

    @action(detail=False, methods=["post"])
    def roi_prediction(self, request):
        campaign = Campaign.objects.get(pk=request.data["campaign_id"])
        return Response({"campaign": campaign.id, "predicted_roi": ROIPredictionService.predict_campaign_roi(campaign)})
