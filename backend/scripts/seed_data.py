from datetime import date, timedelta

from django.contrib.auth import get_user_model

from apps.accounts.models import BrandProfile, InfluencerProfile
from apps.campaigns.models import Campaign, CampaignInvitation
from apps.insights.models import Analytics, Payment


def run():
    User = get_user_model()
    admin, _ = User.objects.get_or_create(email="admin@example.com", defaults={"username": "admin", "role": "ADMIN", "is_staff": True, "is_superuser": True})
    admin.set_password("AdminPass123")
    admin.save()

    brand_user, _ = User.objects.get_or_create(email="brand@example.com", defaults={"username": "brand", "role": "BRAND"})
    brand_user.set_password("BrandPass123")
    brand_user.save()
    brand, _ = BrandProfile.objects.get_or_create(user=brand_user, defaults={"company_name": "Nova Cosmetics", "industry": "Beauty", "location": "Mumbai", "monthly_budget": 120000})

    influencers = []
    for index, data in enumerate(
        [
            ("Asha Creates", "Beauty", "Mumbai", 95000, 5.8, 25000),
            ("Ravi Reels", "Fitness", "Bengaluru", 140000, 4.2, 30000),
            ("Meera Eats", "Food", "Delhi", 72000, 6.4, 18000),
        ]
    ):
        user, _ = User.objects.get_or_create(email=f"influencer{index + 1}@example.com", defaults={"username": f"influencer{index + 1}", "role": "INFLUENCER"})
        user.set_password("InfluencerPass123")
        user.save()
        profile, _ = InfluencerProfile.objects.get_or_create(
            user=user,
            defaults={"display_name": data[0], "niche": data[1], "location": data[2], "followers": data[3], "engagement_rate": data[4], "average_rate": data[5], "is_verified": True},
        )
        influencers.append(profile)

    campaign, _ = Campaign.objects.get_or_create(
        brand=brand,
        title="Glow Launch 2026",
        defaults={"description": "Launch campaign for a new skincare line.", "niche": "Beauty", "budget": 150000, "start_date": date.today(), "end_date": date.today() + timedelta(days=30), "status": "ACTIVE"},
    )
    CampaignInvitation.objects.get_or_create(campaign=campaign, influencer=influencers[0], defaults={"invited_by": brand_user, "status": "ACCEPTED", "proposed_rate": 25000})
    Analytics.objects.get_or_create(campaign=campaign, influencer=influencers[0], defaults={"impressions": 82000, "clicks": 3900, "conversions": 410, "spend": 25000, "revenue": 94000, "engagement_rate": 5.9})
    Payment.objects.get_or_create(campaign=campaign, influencer=influencers[0], defaults={"amount": 25000, "status": "PENDING"})
