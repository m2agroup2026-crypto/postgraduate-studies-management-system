from django.db import migrations, models

NAVIGATION_CONFIGURATION = {
    "overview": ("", True),
    "students": ("students.view", True),
    "theses": ("theses.view", True),
    "committees": ("committees.view", True),
    "reports": ("reports.view", False),
    "settings": ("dashboard.manage", True),
}


def configure_navigation(apps, schema_editor):
    navigation = apps.get_model("core", "DashboardNavigationItem")
    for key, (permission, operational) in NAVIGATION_CONFIGURATION.items():
        navigation.objects.filter(key=key).update(
            required_permission=permission,
            is_operational=operational,
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0005_alter_approvalaction_action")]

    operations = [
        migrations.AddField(
            model_name="dashboardnavigationitem",
            name="is_operational",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(configure_navigation, migrations.RunPython.noop),
    ]
