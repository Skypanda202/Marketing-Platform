from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        BRAND = "BRAND", "Brand"
        INFLUENCER = "INFLUENCER", "Influencer"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.INFLUENCER)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class BrandProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="brand_profile")
    company_name = models.CharField(max_length=160)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="influencer_profile")
    display_name = models.CharField(max_length=160)
    niche = models.CharField(max_length=120, db_index=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, db_index=True)
    portfolio = models.FileField(upload_to="portfolios/", blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    followers = models.PositiveIntegerField(default=0, db_index=True)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_index=True)
    audience_demographics = models.JSONField(default=dict, blank=True)
    average_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    fake_follower_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sentiment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["niche", "location"]),
            models.Index(fields=["followers", "engagement_rate"]),
        ]

    def __str__(self):
        return self.display_name
