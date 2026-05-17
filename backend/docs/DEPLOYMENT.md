# Deployment Guide

1. Provision PostgreSQL and set `DATABASE_URL`.
2. Set secure production values for `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run `python manage.py migrate`.
5. Create an admin with `python manage.py createsuperuser`.
6. Collect static files with `python manage.py collectstatic --noinput`.
7. Run with Gunicorn: `gunicorn config.wsgi:application`.
8. Put the app behind HTTPS with Nginx, Caddy, Render, Railway, Fly.io, or a similar platform.

Recommended production additions:

- Managed PostgreSQL backups.
- Object storage for media uploads.
- SMTP provider for password resets.
- Sentry or OpenTelemetry for error monitoring.
- Celery plus Redis for heavy AI jobs and email sending.
