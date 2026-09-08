from django.db import migrations, models


def seed_dashboard_configuration(apps, schema_editor):
    Navigation = apps.get_model("core", "DashboardNavigationItem")
    Metric = apps.get_model("core", "DashboardMetricCard")

    navigation = [
        ("overview", "نظرة عامة", "Overview", "/", "LayoutDashboard", 10),
        ("students", "الطلاب", "Students", "/students", "Users", 20),
        ("theses", "الرسائل العلمية", "Theses", "/theses", "BookOpen", 30),
        ("committees", "اللجان والمناقشات", "Committees & Defenses", "/committees", "CalendarDays", 40),
        ("reports", "التقارير", "Reports", "/reports", "BarChart3", 50),
        ("settings", "الإعدادات", "Settings", "/settings", "Settings", 60),
    ]
    for key, label_ar, label_en, route, icon, sort_order in navigation:
        Navigation.objects.get_or_create(
            key=key,
            defaults={
                "label_ar": label_ar,
                "label_en": label_en,
                "route": route,
                "icon": icon,
                "sort_order": sort_order,
                "is_active": True,
            },
        )

    metrics = [
        ("students", "الطلاب النشطون", "Active students", "Users", 10),
        ("theses", "الرسائل المسجلة", "Registered theses", "BookOpen", 20),
        ("defenses", "المناقشات القادمة", "Upcoming defenses", "CalendarDays", 30),
        ("pending", "ملفات تحتاج متابعة", "Files requiring follow-up", "GraduationCap", 40),
    ]
    for key, label_ar, label_en, icon, sort_order in metrics:
        Metric.objects.get_or_create(
            key=key,
            defaults={
                "label_ar": label_ar,
                "label_en": label_en,
                "icon": icon,
                "sort_order": sort_order,
                "is_active": True,
            },
        )


def unseed_dashboard_configuration(apps, schema_editor):
    apps.get_model("core", "DashboardNavigationItem").objects.all().delete()
    apps.get_model("core", "DashboardMetricCard").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0003_workflowstatus")]

    operations = [
        migrations.CreateModel(
            name="DashboardNavigationItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=80, unique=True)),
                ("label_ar", models.CharField(max_length=150)),
                ("label_en", models.CharField(blank=True, max_length=150)),
                ("route", models.CharField(default="/", max_length=180)),
                ("icon", models.CharField(blank=True, default="LayoutDashboard", max_length=60)),
                ("required_permission", models.CharField(blank=True, max_length=100)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.CreateModel(
            name="DashboardMetricCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(choices=[("students", "الطلاب النشطون"), ("theses", "الرسائل المسجلة"), ("defenses", "المناقشات القادمة"), ("pending", "ملفات تحتاج متابعة")], max_length=32, unique=True)),
                ("label_ar", models.CharField(max_length=150)),
                ("label_en", models.CharField(blank=True, max_length=150)),
                ("icon", models.CharField(blank=True, max_length=60)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
        migrations.RunPython(seed_dashboard_configuration, unseed_dashboard_configuration),
    ]
