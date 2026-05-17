from rest_framework import serializers

from .models import Analytics, Payment, Review


class AnalyticsSerializer(serializers.ModelSerializer):
    roi = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = Analytics
        fields = "__all__"
        read_only_fields = ["id", "recorded_at", "roi"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["id", "created_at", "paid_at"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["id", "reviewer", "created_at"]
