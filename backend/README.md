# نظام إدارة الدراسات العليا – كلية الطب بجامعة أسيوط

نظام ويب داخلي لإدارة ملفات طلاب الدراسات العليا ودورتهم الأكاديمية، مبني باستخدام Django وPostgreSQL.

## متطلبات التطوير

- Python 3.12 أو 3.13
- PostgreSQL
- `uv`

## التشغيل المحلي

```bash
cp .env.example .env
uv sync --dev
set -a && source .env && set +a
uv run python manage.py migrate
uv run python manage.py runserver
```

فحص الصحة متاح على `/health/`، ولوحة Django الإدارية على `/admin/`.

## فحوصات الجودة

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

## تنبيه الخصوصية

لا تضع بيانات طلاب حقيقية أو ملفات Excel تشغيلية أو نسخ قواعد البيانات داخل المستودع. استخدم بيانات مولدة للاختبارات والتطوير.

راجع مواصفات النظام وخطة التنفيذ داخل `docs/superpowers/` قبل إضافة الوحدات.
