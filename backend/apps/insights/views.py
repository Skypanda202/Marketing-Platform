from django.db.models import Avg, Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Analytics, Payment, Review
from .serializers import AnalyticsSerializer, PaymentSerializer, ReviewSerializer


class AnalyticsViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["campaign", "influencer"]
    ordering_fields = ["recorded_at", "impressions", "clicks", "conversions", "revenue"]

    def get_queryset(self):
        qs = Analytics.objects.select_related("campaign", "campaign__brand", "influencer")
        user = self.request.user
        if user.role == "ADMIN":
            return qs
        if user.role == "BRAND":
            return qs.filter(campaign__brand__user=user)
        return qs.filter(influencer__user=user)

    @action(detail=False, methods=["get"])
    def overview(self, request):
        qs = self.get_queryset()
        totals = qs.aggregate(
            impressions=Sum("impressions"),
            clicks=Sum("clicks"),
            conversions=Sum("conversions"),
            spend=Sum("spend"),
            revenue=Sum("revenue"),
            engagement_rate=Avg("engagement_rate"),
        )
        spend = totals.get("spend") or 0
        revenue = totals.get("revenue") or 0
        totals["roi"] = 0 if spend == 0 else round(((revenue - spend) / spend) * 100, 2)
        return Response(totals)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["campaign", "influencer", "status"]
    ordering_fields = ["amount", "created_at"]

    def get_queryset(self):
        qs = Payment.objects.select_related("campaign", "campaign__brand", "influencer")
        user = self.request.user
        if user.role == "ADMIN":
            return qs
        if user.role == "BRAND":
            return qs.filter(campaign__brand__user=user)
        return qs.filter(influencer__user=user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["campaign", "influencer", "rating"]
    ordering_fields = ["rating", "created_at"]

    def get_queryset(self):
        qs = Review.objects.select_related("campaign", "reviewer", "influencer")
        if self.request.user.role == "ADMIN":
            return qs
        return qs.filter(reviewer=self.request.user) | qs.filter(influencer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
