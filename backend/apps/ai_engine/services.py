import math
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:
    @staticmethod
    def rank_influencers(queryset, brand_user):
        brand_text = ""
        if hasattr(brand_user, "brand_profile"):
            brand = brand_user.brand_profile
            brand_text = f"{brand.industry} {brand.description} {brand.location}"
        influencers = list(queryset)
        if not influencers:
            return queryset
        docs = [brand_text or "brand campaign marketing"] + [
            f"{item.niche} {item.bio} {item.location} {item.followers} {item.engagement_rate}" for item in influencers
        ]
        vectors = TfidfVectorizer(stop_words="english").fit_transform(docs)
        semantic_scores = cosine_similarity(vectors[0], vectors[1:]).flatten()
        scored_ids = []
        for influencer, semantic in zip(influencers, semantic_scores):
            reach = math.log10(max(influencer.followers, 1)) / 7
            engagement = min(float(influencer.engagement_rate) / 10, 1)
            trust = 1 - min(float(influencer.fake_follower_score) / 100, 1)
            score = round((semantic * 0.35 + reach * 0.25 + engagement * 0.3 + trust * 0.1) * 100, 2)
            influencer.recommendation_score = score
            scored_ids.append((influencer.id, score))
        ordering = {item_id: index for index, (item_id, _) in enumerate(sorted(scored_ids, key=lambda row: row[1], reverse=True))}
        return sorted(influencers, key=lambda item: ordering[item.id])


class FakeEngagementService:
    @staticmethod
    def score(followers, engagement_rate, recent_likes=None, recent_comments=None):
        recent_likes = recent_likes or []
        recent_comments = recent_comments or []
        like_variance = float(np.var(recent_likes)) if recent_likes else 0
        comment_variance = float(np.var(recent_comments)) if recent_comments else 0
        expected_engagement = max(math.log10(max(followers, 1)) * 0.8, 1)
        low_engagement_penalty = max(expected_engagement - float(engagement_rate), 0) * 8
        uniformity_penalty = 15 if like_variance < 50 and len(recent_likes) >= 5 else 0
        comment_penalty = 10 if comment_variance < 10 and len(recent_comments) >= 5 else 0
        return round(min(low_engagement_penalty + uniformity_penalty + comment_penalty, 100), 2)


class SentimentService:
    POSITIVE = {"love", "great", "excellent", "amazing", "trusted", "happy", "best", "recommend"}
    NEGATIVE = {"bad", "fake", "poor", "angry", "scam", "worst", "hate", "late"}

    @classmethod
    def analyze(cls, text):
        tokens = re.findall(r"[a-zA-Z']+", text.lower())
        if not tokens:
            return {"score": 0, "label": "neutral"}
        positive = sum(token in cls.POSITIVE for token in tokens)
        negative = sum(token in cls.NEGATIVE for token in tokens)
        score = round(((positive - negative) / len(tokens)) * 100, 2)
        label = "positive" if score > 2 else "negative" if score < -2 else "neutral"
        return {"score": score, "label": label}


class ROIPredictionService:
    @staticmethod
    def predict_campaign_roi(campaign):
        x = np.array([[1000, 2], [5000, 4], [10000, 5], [20000, 7], [50000, 9]], dtype=float)
        y = np.array([8, 18, 31, 49, 76], dtype=float)
        model = LinearRegression().fit(x, y)
        budget = float(campaign.budget or 0)
        duration = max((campaign.end_date - campaign.start_date).days, 1)
        return round(float(model.predict(np.array([[budget, duration]], dtype=float))[0]), 2)
