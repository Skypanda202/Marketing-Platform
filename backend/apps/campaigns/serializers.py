from rest_framework import serializers

from apps.accounts.serializers import BrandProfileSerializer, InfluencerProfileSerializer

from .models import Campaign, CampaignInvitation


class CampaignSerializer(serializers.ModelSerializer):
    brand = BrandProfileSerializer(read_only=True)
    invitation_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ["id", "brand", "expected_roi", "created_at", "updated_at"]


class CampaignInvitationSerializer(serializers.ModelSerializer):
    campaign_detail = CampaignSerializer(source="campaign", read_only=True)
    influencer_detail = InfluencerProfileSerializer(source="influencer", read_only=True)

    class Meta:
        model = CampaignInvitation
        fields = "__all__"
        read_only_fields = ["id", "invited_by", "responded_at", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context["request"]
        campaign = attrs.get("campaign") or getattr(self.instance, "campaign", None)
        if request.user.role == "BRAND" and campaign and campaign.brand.user != request.user:
            raise serializers.ValidationError("Brands can only invite influencers to their own campaigns.")
        return attrs
