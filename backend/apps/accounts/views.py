from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.ai_engine.services import RecommendationService

from .models import BrandProfile, InfluencerProfile
from .permissions import IsAdminRole, IsOwnerOrAdmin
from .serializers import BrandProfileSerializer, InfluencerProfileSerializer, LoginSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def _tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user).data, "tokens": self._tokens_for_user(user)}, status=status.HTTP_201_CREATED)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response({"user": UserSerializer(user).data, "tokens": self._tokens_for_user(user)})

    def logout(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token:
            RefreshToken(refresh_token).blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def me(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        return Response(UserSerializer(request.user).data)

    def forgot_password(self, request):
        email = request.data.get("email")
        if email:
            send_mail(
                "Password reset requested",
                "A password reset was requested. Connect this endpoint to your frontend reset flow in production.",
                None,
                [email],
                fail_silently=True,
            )
        return Response({"detail": "If the account exists, a reset email has been sent."})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["role", "is_active", "is_verified"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering_fields = ["created_at", "email"]


class BrandProfileViewSet(viewsets.ModelViewSet):
    serializer_class = BrandProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    search_fields = ["company_name", "industry", "location"]
    filterset_fields = ["industry", "location"]

    def get_queryset(self):
        qs = BrandProfile.objects.select_related("user").order_by("-created_at")
        if self.request.user.role == "ADMIN":
            return qs
        if self.request.user.role == "BRAND":
            return qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InfluencerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = InfluencerProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filterset_fields = ["niche", "location", "is_verified"]
    search_fields = ["display_name", "niche", "location", "bio"]
    ordering_fields = ["followers", "engagement_rate", "average_rate", "created_at"]

    def get_queryset(self):
        qs = InfluencerProfile.objects.select_related("user").order_by("-followers")
        followers_min = self.request.query_params.get("followers_min")
        followers_max = self.request.query_params.get("followers_max")
        engagement_min = self.request.query_params.get("engagement_min")
        if followers_min:
            qs = qs.filter(followers__gte=followers_min)
        if followers_max:
            qs = qs.filter(followers__lte=followers_max)
        if engagement_min:
            qs = qs.filter(engagement_rate__gte=engagement_min)
        if self.request.user.role == "INFLUENCER":
            return qs.filter(user=self.request.user)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.role == "BRAND":
            ranked = RecommendationService.rank_influencers(queryset, request.user)
            page = self.paginate_queryset(ranked)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(ranked, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminRole])
    def verify(self, request, pk=None):
        profile = self.get_object()
        profile.is_verified = True
        profile.user.is_verified = True
        profile.user.save(update_fields=["is_verified"])
        profile.save(update_fields=["is_verified"])
        return Response(self.get_serializer(profile).data)
