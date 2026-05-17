from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Campaign(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        ACTIVE = "ACTIVE", "Active"
        PAUSED = "PAUSED", "Paused"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    brand = models.ForeignKey("accounts.BrandProfile", on_delete=models.CASCADE, related_name="campaigns")
    title = models.CharField(max_length=200)
    description = models.TextField()
    goals = models.TextField(blank=True)
    niche = models.CharField(max_length=120, db_index=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    deliverables = models.JSONField(default=list, blank=True)
    target_locations = models.JSONField(default=list, blank=True)
    expected_roi = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "niche"]), models.Index(fields=["start_date", "end_date"])]

    def __str__(self):
        return self.title


class CampaignInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        COMPLETED = "COMPLETED", "Completed"

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="invitations")
    influencer = models.ForeignKey("accounts.InfluencerProfile", on_delete=models.CASCADE, related_name="invitations")
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sent_invitations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    message = models.TextField(blank=True)
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    submitted_content_url = models.URLField(blank=True)
    submitted_content_notes = models.TextField(blank=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("campaign", "influencer")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.campaign} -> {self.influencer}"
