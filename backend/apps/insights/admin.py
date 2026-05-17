from django.contrib import admin

from .models import Analytics, Payment, Review


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ("campaign", "influencer", "impressions", "clicks", "conversions", "revenue", "recorded_at")
    list_filter = ("recorded_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("campaign", "influencer", "amount", "status", "created_at")
    list_filter = ("status", "created_at")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("campaign", "reviewer", "influencer", "rating", "created_at")
    list_filter = ("rating", "created_at")
