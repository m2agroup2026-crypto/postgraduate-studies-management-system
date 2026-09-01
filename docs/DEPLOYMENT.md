# Production Deployment

## Required environment variables

- `POSTGRES_PASSWORD`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `CORS_ALLOWED_ORIGINS`

## Start

```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml ps
curl -fsS http://127.0.0.1/health/
```

Create the initial accounts through Django Admin or run `seed_demo` only after setting `PGMS_DEMO_PASSWORD`. Never commit real student data or production secrets.

## Mobile builds

Set `EXPO_PUBLIC_API_URL=https://your-domain.example/api/v1`, then use Expo/EAS to produce the Android AAB/APK and iOS archive. Apple distribution requires the institution's Apple Developer account and signing credentials; Android Play distribution requires its signing key.
