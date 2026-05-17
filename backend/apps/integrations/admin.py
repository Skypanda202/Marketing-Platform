from django.contrib import admin

from .models import AdCampaignLaunch, AdPlatformConnection


@admin.register(AdPlatformConnection)
class AdPlatformConnectionAdmin(admin.ModelAdmin):
    list_display = ("owner", "provider", "account_id", "account_name", "is_active", "created_at")
    list_filter = ("provider", "is_active", "created_at")
    search_fields = ("owner__email", "account_id", "account_name")


@admin.register(AdCampaignLaunch)
class AdCampaignLaunchAdmin(admin.ModelAdmin):
    list_display = ("campaign", "connection", "status", "dry_run", "daily_budget", "created_at")
    list_filter = ("status", "dry_run", "connection__provider")
    search_fields = ("campaign__title", "platform_campaign_id")
