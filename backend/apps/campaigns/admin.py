from django.contrib import admin

from .models import Campaign, CampaignInvitation


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "brand", "niche", "budget", "status", "start_date", "end_date")
    list_filter = ("status", "niche", "start_date")
    search_fields = ("title", "description", "brand__company_name")


@admin.register(CampaignInvitation)
class CampaignInvitationAdmin(admin.ModelAdmin):
    list_display = ("campaign", "influencer", "status", "proposed_rate", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("campaign__title", "influencer__display_name")
