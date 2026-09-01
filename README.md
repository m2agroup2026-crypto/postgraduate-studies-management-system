# Postgraduate Studies Management System

منصة عربية افتراضيًا لإدارة الدراسات العليا، تشمل لوحة مدير البرنامج، ولوحة عميد الكلية الأستاذ الدكتور علاء عطية، ولوحة وكيل الكلية لشؤون الدراسات العليا والبحوث الأستاذ الدكتور محمد عبد الباسط خلاف، بالإضافة إلى مساعد ذكي وتطبيق Android وiOS.

## المكونات

- `backend/`: Django REST API + JWT + PostgreSQL.
- `web/`: React enterprise dashboard، عربي RTL افتراضيًا وإنجليزي LTR.
- `mobile/`: Expo React Native لتطبيق Android وiOS.
- `docker-compose.yml`: تشغيل قاعدة البيانات والـAPI والويب معًا.

## التشغيل السريع

```bash
docker compose up --build
```

الويب: `http://localhost:5173`
الـAPI: `http://localhost:8000/api/v1/`
فحص الخدمة: `http://localhost:8000/health/`

حسابات العرض: `director` و`dean` و`vice_dean`. عيّن كلمة المرور الآمنة في المتغير `PGMS_DEMO_PASSWORD` قبل التشغيل.

## الموبايل

```bash
cd mobile
npm install
npm start
```

بعدها اختر Android أو iOS من Expo. معرف الحزمة: `edu.aun.med.pgms`.

## تشغيل Production

انسخ `.env.example` إلى `.env` وعيّن القيم الآمنة والدومين، ثم شغّل:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

يخدم Nginx الواجهة على المنفذ `80` ويوجه `/api/` إلى Django/Gunicorn داخليًا. استخدم Reverse Proxy يدعم HTTPS قبل فتح النظام للمستخدمين.

## الربط الفعلي

- الويب يستخدم `VITE_API_URL`، أو `/api/v1` في حاوية Production.
- الموبايل يستخدم `EXPO_PUBLIC_API_URL` ويخزن JWT داخل Secure Store.
- مؤشرات اللوحات والمساعد الذكي تُقرأ من Django API وفق صلاحية الحساب.
