# Influencer Marketing Platform API

Base URL: `http://localhost:8000/api/`

Interactive OpenAPI docs are available at `/api/docs/` after running the server.

## Authentication

- `POST /api/auth/register/` creates an Admin, Brand, or Influencer account and returns JWT tokens.
- `POST /api/auth/` logs in with `email` and `password`.
- `POST /api/auth/token/refresh/` refreshes an access token.
- `POST /api/auth/logout/` blacklists a refresh token.
- `GET /api/auth/me/` returns the current user.
- `POST /api/auth/forgot-password/` sends a reset email placeholder.

Use `Authorization: Bearer <access_token>` for protected endpoints.

## Core Resources

- `/api/users/` admin-only user management.
- `/api/brands/` brand profile CRUD.
- `/api/influencers/` influencer search with `niche`, `location`, `followers_min`, `followers_max`, `engagement_min`, `search`, and `ordering`.
- `/api/campaigns/` campaign CRUD and `POST /api/campaigns/{id}/predict_roi/`.
- `/api/invitations/` invite influencers, accept/reject invitations, and submit content.
- `/api/messages/` campaign-aware messaging and `/api/messages/thread/?user=<id>`.
- `/api/notifications/` user notifications and mark-read actions.
- `/api/analytics/` campaign metrics and `/api/analytics/overview/`.
- `/api/payments/` influencer earnings and payment tracking.
- `/api/reviews/` post-campaign reviews.
- `/api/ai/recommendations/`, `/api/ai/sentiment/`, `/api/ai/fake_engagement/`, and `/api/ai/roi_prediction/`.
- `/api/feed/`, `/api/comments/`, and `/api/follows/` provide Instagram-style brand and creator social networking.
- `/api/integrations/connections/` stores Meta and Google ad account connections.
- `/api/integrations/oauth/meta/start/` and `/api/integrations/oauth/google/start/` return OAuth authorization URLs.
- `/api/integrations/launches/` prepares ad launches and `/api/integrations/launches/{id}/submit/` validates or submits platform campaigns.

## Filtering And Pagination

List endpoints use DRF page-number pagination:

```text
GET /api/influencers/?niche=Beauty&followers_min=50000&engagement_min=3&ordering=-followers
```

Responses follow:

```json
{
  "count": 24,
  "next": "http://localhost:8000/api/influencers/?page=2",
  "previous": null,
  "results": []
}
```
