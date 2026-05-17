from urllib.parse import urlencode

import requests
from django.conf import settings
from decimal import Decimal


class MetaAdsService:
    @staticmethod
    def auth_url(state):
        params = {
            "client_id": settings.META_APP_ID,
            "redirect_uri": settings.META_REDIRECT_URI,
            "state": state,
            "scope": "email,public_profile,ads_management,ads_read,business_management,instagram_basic",
            "response_type": "code",
        }
        return f"https://www.facebook.com/{settings.META_GRAPH_VERSION}/dialog/oauth?{urlencode(params)}"

    @staticmethod
    def exchange_code(code):
        response = requests.get(
            f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/oauth/access_token",
            params={
                "client_id": settings.META_APP_ID,
                "client_secret": settings.META_APP_SECRET,
                "redirect_uri": settings.META_REDIRECT_URI,
                "code": code,
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_paused_campaign(connection, launch):
        if launch.dry_run:
            return {"dry_run": True, "provider": "META", "message": "Validated. Set dry_run=false to submit to Meta."}
        ad_account_id = connection.account_id if connection.account_id.startswith("act_") else f"act_{connection.account_id}"
        response = requests.post(
            f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/{ad_account_id}/campaigns",
            data={
                "name": launch.campaign.title,
                "objective": launch.objective,
                "status": "PAUSED",
                "special_ad_categories": "[]",
                "access_token": connection.access_token,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


class GoogleAdsService:
    API_VERSION = "v22"

    @staticmethod
    def auth_url(state):
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
            "scope": "openid email profile https://www.googleapis.com/auth/adwords",
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    @staticmethod
    def exchange_code(code):
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_paused_campaign(connection, launch):
        if launch.dry_run:
            return {
                "dry_run": True,
                "provider": "GOOGLE",
                "message": "Validated. Set dry_run=false to create a paused Google Ads campaign.",
                "customer_id": connection.account_id,
                "developer_token_configured": bool(settings.GOOGLE_ADS_DEVELOPER_TOKEN),
            }
        headers = {
            "Authorization": f"Bearer {connection.access_token}",
            "developer-token": settings.GOOGLE_ADS_DEVELOPER_TOKEN,
            "Content-Type": "application/json",
        }
        manager_customer_id = connection.metadata.get("manager_customer_id")
        if manager_customer_id:
            headers["login-customer-id"] = manager_customer_id
        customer_id = connection.account_id.replace("-", "")
        budget_response = requests.post(
            f"https://googleads.googleapis.com/{GoogleAdsService.API_VERSION}/customers/{customer_id}/campaignBudgets:mutate",
            headers=headers,
            json={
                "operations": [
                    {
                        "create": {
                            "name": f"{launch.campaign.title} Budget",
                            "deliveryMethod": "STANDARD",
                            "amountMicros": int(Decimal(launch.daily_budget) * Decimal("1000000")),
                        }
                    }
                ]
            },
            timeout=30,
        )
        budget_response.raise_for_status()
        budget_resource = budget_response.json()["results"][0]["resourceName"]
        campaign_response = requests.post(
            f"https://googleads.googleapis.com/{GoogleAdsService.API_VERSION}/customers/{customer_id}/campaigns:mutate",
            headers=headers,
            json={
                "operations": [
                    {
                        "create": {
                            "name": launch.campaign.title,
                            "campaignBudget": budget_resource,
                            "advertisingChannelType": "SEARCH",
                            "status": "PAUSED",
                            "manualCpc": {},
                            "networkSettings": {
                                "targetGoogleSearch": True,
                                "targetSearchNetwork": True,
                                "targetContentNetwork": True,
                                "targetPartnerSearchNetwork": False,
                            },
                        }
                    }
                ]
            },
            timeout=30,
        )
        campaign_response.raise_for_status()
        return campaign_response.json()
