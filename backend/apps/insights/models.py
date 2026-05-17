from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Analytics(models.Model):
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE, related_name="analytics")
    influencer = models.ForeignKey("accounts.InfluencerProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="analytics")
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    spend = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Analytics"
        ordering = ["-recorded_at"]

    @property
    def roi(self):
        return 0 if self.spend == 0 else round(((self.revenue - self.spend) / self.spend) * 100, 2)


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE, related_name="payments")
    influencer = models.ForeignKey("accounts.InfluencerProfile", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_reference = models.CharField(max_length=120, blank=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Review(models.Model):
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_given")
    influencer = models.ForeignKey("accounts.InfluencerProfile", on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("campaign", "reviewer", "influencer")
        ordering = ["-created_at"]
