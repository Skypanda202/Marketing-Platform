from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BrandProfile, InfluencerProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_verified", "is_active", "created_at")
    list_filter = ("role", "is_verified", "is_active")
    search_fields = ("email", "username", "first_name", "last_name")
    fieldsets = UserAdmin.fieldsets + (("Platform", {"fields": ("role", "avatar", "phone", "is_verified")}),)


@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "industry", "location", "monthly_budget")
    search_fields = ("company_name", "industry", "location")


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "niche", "followers", "engagement_rate", "is_verified", "fake_follower_score")
    list_filter = ("niche", "location", "is_verified")
    search_fields = ("display_name", "niche", "location")
