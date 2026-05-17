# Influencer Marketing Platform for Seamless Collaboration and Campaign Management

Production-ready full-stack scaffold for brands, influencers, and admins to manage influencer campaigns, discovery, invitations, messaging, analytics, verification, payments, reviews, and AI-assisted decisions.

## Project Structure

```text
backend/
  apps/
    accounts/          users, roles, brand profiles, influencer profiles
    campaigns/         campaigns and invitations
    communications/    messaging and notifications
    insights/          analytics, payments, reviews
    ai_engine/         recommendation, sentiment, fake engagement, ROI services
  config/              Django settings, URLs, ASGI/WSGI
  docs/                API, schema, deployment notes
  scripts/             dummy seed data
frontend/
  src/
    api/               Axios client and service layer
    components/        reusable cards, charts, tables, skeletons
    context/           auth and theme contexts
    layouts/           app shell
    pages/             role dashboards and feature pages
    routes/            protected route guards
```

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

PostgreSQL is configured through `DATABASE_URL`. The local development env now uses port `5432` and the password you provided:

```env
DATABASE_URL=postgres://postgres:Password1@localhost:5432/influencer_platform
```

Create the database before running migrations:

```sql
CREATE DATABASE influencer_platform;
```

API docs:

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

## Dummy Data

After migrating, load sample data in a Django shell:

```bash
python manage.py shell
```

```python
from scripts.seed_data import run
run()
```

Demo credentials:

```text
admin@example.com / AdminPass123
brand@example.com / BrandPass123
influencer1@example.com / InfluencerPass123
```

## Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend runs at `http://127.0.0.1:5173` and talks to `VITE_API_URL`.

## Security Notes

- JWT authentication with rotating refresh tokens and token blacklist.
- Passwords are hashed by Django's auth system.
- Role-based access control is enforced in DRF querysets and permissions.
- CORS origins are environment-driven.
- ORM query construction protects against SQL injection.
- Django middleware provides CSRF, clickjacking, session, and XSS-related protections.
- Keep `SECRET_KEY`, database credentials, and email credentials outside source control.

## Meta, Instagram, Facebook, And Google Ads

The backend includes production-ready integration boundaries for:

- Meta Marketing API campaign launch through `/api/integrations/launches/{id}/submit/`.
- Facebook and Instagram OAuth start URL through `/api/integrations/oauth/meta/start/`.
- Google OAuth start URL through `/api/integrations/oauth/google/start/`.
- Manual ad account connection management through `/api/integrations/connections/`.

Required env values:

```env
META_APP_ID=1514367733549829
META_APP_SECRET=your_meta_app_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_ADS_DEVELOPER_TOKEN=your_google_ads_developer_token
```

New ad launches default to `dry_run=true`. This validates launch payloads without spending money. Set `dry_run=false` only after the Meta app permissions, Google Ads developer token, OAuth consent, billing, and ad account access are approved.

References:

- Meta Marketing API requires user/system-user access tokens and permissions such as `ads_management` for write operations.
- Google Ads API requires OAuth credentials, a manager or client account, and a developer token.

## Documentation

- Backend API: [backend/docs/API.md](backend/docs/API.md)
- Database schema: [backend/docs/SCHEMA.md](backend/docs/SCHEMA.md)
- Deployment: [backend/docs/DEPLOYMENT.md](backend/docs/DEPLOYMENT.md)
