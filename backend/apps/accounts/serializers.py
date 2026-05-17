from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import BrandProfile, InfluencerProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "avatar",
            "phone",
            "is_verified",
            "created_at"
        ]
        read_only_fields = ["id", "is_verified", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    company_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    display_name = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    niche = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "company_name",
            "display_name",
            "niche"
        ]

        read_only_fields = ["id"]

    def validate(self, attrs):
        role = attrs.get("role")

        if role == User.Role.BRAND and not attrs.get("company_name"):
            raise serializers.ValidationError({
                "company_name": "Company name is required for brand accounts."
            })

        if role == User.Role.INFLUENCER and not attrs.get("display_name"):
            raise serializers.ValidationError({
                "display_name": "Display name is required for influencer accounts."
            })

        return attrs

    def create(self, validated_data):
        company_name = validated_data.pop("company_name", "")
        display_name = validated_data.pop("display_name", "")
        niche = validated_data.pop("niche", "Lifestyle")

        password = validated_data.pop("password")

        user = User(**validated_data)

        # HASH PASSWORD
        user.set_password(password)

        user.save()

        # CREATE ROLE PROFILE
        if user.role == User.Role.BRAND:
            BrandProfile.objects.create(
                user=user,
                company_name=company_name
            )

        elif user.role == User.Role.INFLUENCER:
            InfluencerProfile.objects.create(
                user=user,
                display_name=display_name,
                niche=niche
            )

        return user


# FIXED LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This account is disabled."
            )

        attrs["user"] = user

        return attrs


class BrandProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BrandProfile
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at"
        ]


class InfluencerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    recommendation_score = serializers.FloatField(
        read_only=True,
        required=False
    )

    class Meta:
        model = InfluencerProfile
        fields = "__all__"

        read_only_fields = [
            "id",
            "user",
            "fake_follower_score",
            "sentiment_score",
            "is_verified",
            "created_at",
            "updated_at"
        ]