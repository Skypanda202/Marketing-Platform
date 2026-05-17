from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import AuthViewSet, BrandProfileViewSet, InfluencerProfileViewSet, UserViewSet
from apps.ai_engine.views import AIViewSet
from apps.campaigns.views import CampaignInvitationViewSet, CampaignViewSet
from apps.communications.views import MessageViewSet, NotificationViewSet
from apps.insights.views import AnalyticsViewSet, PaymentViewSet, ReviewViewSet
from apps.integrations.views import AdCampaignLaunchViewSet, AdPlatformConnectionViewSet, SocialAuthViewSet
from apps.social.views import CommentViewSet, FeedPostViewSet, FollowViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("brands", BrandProfileViewSet, basename="brands")
router.register("influencers", InfluencerProfileViewSet, basename="influencers")
router.register("campaigns", CampaignViewSet, basename="campaigns")
router.register("invitations", CampaignInvitationViewSet, basename="invitations")
router.register("messages", MessageViewSet, basename="messages")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("analytics", AnalyticsViewSet, basename="analytics")
router.register("payments", PaymentViewSet, basename="payments")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("ai", AIViewSet, basename="ai")
router.register("feed", FeedPostViewSet, basename="feed")
router.register("comments", CommentViewSet, basename="comments")
router.register("follows", FollowViewSet, basename="follows")
router.register("integrations/connections", AdPlatformConnectionViewSet, basename="ad-connections")
router.register("integrations/launches", AdCampaignLaunchViewSet, basename="ad-launches")
router.register("integrations/oauth", SocialAuthViewSet, basename="social-oauth")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("api/auth/register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path("api/auth/logout/", AuthViewSet.as_view({"post": "logout"}), name="logout"),
    path("api/auth/me/", AuthViewSet.as_view({"get": "me"}), name="me"),
    path("api/auth/forgot-password/", AuthViewSet.as_view({"post": "forgot_password"}), name="forgot-password"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
