from rest_framework import serializers

from .models import AdCampaignLaunch, AdPlatformConnection


class AdPlatformConnectionSerializer(serializers.ModelSerializer):
    has_access_token = serializers.SerializerMethodField()

    class Meta:
        model = AdPlatformConnection
        fields = ["id", "owner", "provider", "account_id", "account_name", "has_access_token", "scopes", "is_active", "metadata", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at", "has_access_token"]

    def get_has_access_token(self, obj):
        return bool(obj.access_token)


class AdCampaignLaunchSerializer(serializers.ModelSerializer):
    connection_detail = AdPlatformConnectionSerializer(source="connection", read_only=True)

    class Meta:
        model = AdCampaignLaunch
        fields = "__all__"
        read_only_fields = ["id", "platform_campaign_id", "platform_response", "status", "created_at", "updated_at"]
