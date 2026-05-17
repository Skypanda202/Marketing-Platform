from django.conf import settings
from django.db import models


class AdPlatformConnection(models.Model):
    class Provider(models.TextChoices):
        META = "META", "Meta / Facebook / Instagram"
        GOOGLE = "GOOGLE", "Google Ads"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ad_connections")
    provider = models.CharField(max_length=20, choices=Provider.choices)
    account_id = models.CharField(max_length=120)
    account_name = models.CharField(max_length=180, blank=True)
    access_token = models.TextField(blank=True)
    refresh_token = models.TextField(blank=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)
    scopes = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("owner", "provider", "account_id")
        ordering = ["provider", "account_name"]

    def __str__(self):
        return f"{self.owner.email} - {self.provider} - {self.account_id}"


class AdCampaignLaunch(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        VALIDATED = "VALIDATED", "Validated"
        SUBMITTED = "SUBMITTED", "Submitted"
        FAILED = "FAILED", "Failed"

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE, related_name="ad_launches")
    connection = models.ForeignKey(AdPlatformConnection, on_delete=models.CASCADE, related_name="launches")
    objective = models.CharField(max_length=80, default="OUTCOME_TRAFFIC")
    daily_budget = models.DecimalField(max_digits=12, decimal_places=2)
    destination_url = models.URLField()
    audience = models.JSONField(default=dict, blank=True)
    creative = models.JSONField(default=dict, blank=True)
    platform_campaign_id = models.CharField(max_length=120, blank=True)
    platform_response = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    dry_run = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
